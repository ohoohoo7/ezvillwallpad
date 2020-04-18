import paho.mqtt.client as mqtt
import json
import time
import asyncio

share_dir = '/share'
config_dir = '/data'
data_dir = '/ezvill2mqtt'

HA_TOPIC = 'ezvill'
STATE_TOPIC = HA_TOPIC + '/{}/{}/state'
ELFIN_TOPIC = 'ew11'
ELFIN_SEND_TOPIC = ELFIN_TOPIC + '/send'


def log(string):
    date = time.strftime('%Y-%m-%d %p %I:%M:%S', time.localtime(time.time()+9*60*60))
    print('[{}] {}'.format(date, string))
    return

def do_work(config, device_list):
    debug = config['DEBUG']
    mqtt_log = config['mqtt_log']
    elfin_log = config['elfin_log']
    data_prefix = config['data_prefix']
        
    """def make_device_info(device):
        num = device.get('Number')
        seperator = device.get('deviceSEPERATOR')
        arr = {cmd + onoff: device.get(cmd + onoff) for cmd in ['command', 'state'] for onoff in ['ON', 'OFF']}
        arr['Num'] = num
        arr['seperator'] = seperator
        arr['seperatorstartnum'] = device.get('seperatorSTARTNUM')
        if num > 1:
        	for k in range(num):
        		arr['statenum{}'.format(k+1)] = device.get('statenum{}'.format(k+1))
        return arr"""
    
    DEVICE_LISTS = device_list #{}
    for name in device_list:
        #device_info = make_device_info(device_list[name])
        #if device_info:
        #    DEVICE_LISTS[name] = device_info
   
    seperator_list = {DEVICE_LISTS[name]['deviceSEPERATOR']: name for name in DEVICE_LISTS}
    log('----------------------')
    log('Registered device lists..')
    log('DEVICE_LISTS: {}'.format(DEVICE_LISTS))
    log('----------------------')

    HOMESTATE = {}
    QUEUE = []
    COLLECTDATA = {'cond': find_signal, 'data': [], 'EVtime': time.time(), 'LastRecv': time.time_ns()}

    async def recv_from_HA(topics, value):
        key = topics[1] + topics[2]
        device = topics[1][:-1]
        idx = int(topics[1][-1])
        if mqtt_log:
            log('[LOG] HA >> MQTT : {} -> {}'.format('/'.join(topics), value))
        try:
            if device in DEVICE_LISTS:
                if HOMESTATE.get(key) and value != HOMESTATE.get(key):
                    sendcmd = DEVICE_LISTS[device].get('command' + value)
                    if sendcmd:
                        recvcmd = [DEVICE_LISTS[device].get('state' + value, 'NULL')]
                        QUEUE.append({'sendcmd': sendcmd, 'recvcmd': recvcmd, 'count': 0})
                        if debug:
                            log('[DEBUG] Queued ::: sendcmd: {}, recvcmd: {}'.format(sendcmd, recvcmd))
                else:
                    if debug:
                        log('[DEBUG] {} is already set: {}'.format(key, value))
            else:
                if debug:
                    log('[DEBUG] There is no commands for {}'.format('/'.join(topics)))
        except Exception as err:
            log('[ERROR] mqtt_on_message(): {}'.format(err))

    async def recv_from_elfin(data):
        COLLECTDATA['LastRecv'] = time.time_ns()
        if data:
            if elfin_log:
                log('[SIGNAL] receved: {}'.format(data))
            if len(data) > 1:
                for kk in range(len(data)):
                    device_seperator = data[kk][2:6]
                    if device_seperator in seperator_list:
                        device_name = seperator_list[device_seperator]
                        num = DEVICE_LISTS[device_name]['Number']
                        if num == 1:
                            #state = [DEVICE_LISTS[device_name]['stateOFF']] + [DEVICE_LISTS[device_name]['stateON']]
                            fulldata = data_prefix + data[kk]
                            if fulldata == DEVICE_LISTS[device_name]['stateOFF']:
                                #index = state.index(fulldata)
                                #onoff, index = ['OFF', index] if index < num else ['ON', index - num]
                                await update_state(device_name, 'OFF')
                            elif fulldata == DEVICE_LISTS[device_name]['stateON']:
                            	await update_state(device_name, 'ON')
                        else:
                        	for kkk in range(num):
                                if data[kk][int(DEVICE_LIST[device_name]['stateNUM{}'.format(kkk+1))-len(data_prefix)-1] == '0':
                                    await update_state(device_name[:-1]+'{}'.format(kkk+1), 'OFF')
                                else:
                                    await update_state(device_name[:-1]+'{}'.format(kkk+1), 'ON')

    async def update_state(device, onoff):
        state = 'power'
        deviceID = device
        key = deviceID + state

        if onoff != HOMESTATE.get(key):
            HOMESTATE[key] = onoff
            topic = STATE_TOPIC.format(deviceID, state)
            mqtt_client.publish(topic, onoff.encode())
            if mqtt_log:
                log('[LOG] MQTT >> HA : {} >> {}'.format(topic, onoff))
        else:
            if debug:
                log('[DEBUG] {} is already set: {}'.format(deviceID, onoff))
        return

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log("MQTT connection successful!!")
            client.subscribe([(HA_TOPIC + '/#', 0), (ELFIN_TOPIC + '/recv', 0), (ELFIN_TOPIC + '/send', 1)])
        else:
            errcode = {1: 'Connection refused - incorrect protocol version',
                       2: 'Connection refused - invalid client identifier',
                       3: 'Connection refused - server unavailable',
                       4: 'Connection refused - bad username or password',
                       5: 'Connection refused - not authorised'}
            log(errcode[rc])

    def on_message(client, userdata, msg):
        topics = msg.topic.split('/')
        try:
            if topics[0] == HA_TOPIC and topics[-1] == 'command':
                asyncio.run(recv_from_HA(topics, msg.payload.decode('utf-8')))
            elif topics[0] == ELFIN_TOPIC and topics[-1] == 'recv':
                asyncio.run(recv_from_elfin(msg.payload.hex().upper().split(data_seperator)))
        except:
            pass

    mqtt_client = mqtt.Client('commax-mqtt2elfin-python')
    mqtt_client.username_pw_set(config['mqtt_id'], config['mqtt_password'])
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect_async(config['mqtt_server'])
    mqtt_client.loop_start()

    async def send_to_elfin():
        while True:
            try:
                if QUEUE and time.time_ns() - COLLECTDATA['LastRecv'] > 100000000:
                    send_data = QUEUE.pop(0)
                    if elfin_log:
                        log('[SIGNAL] Send a signal: {}'.format(send_data))
                    mqtt_client.publish(ELFIN_SEND_TOPIC, bytes.fromhex(send_data['sendcmd']))
                    await asyncio.sleep(0.1)
                    if send_data['count'] < 3:
                        send_data['count'] = send_data['count'] + 1
                        QUEUE.append(send_data)
                    else:
                        if elfin_log:
                            log('[SIGNAL] Send over 3 times. Send Failure. Delete a queue: {}'.format(send_data))
            except Exception as err:
                log('[ERROR] send_to_elfin(): {}'.format(err))
                return True
            await asyncio.sleep(0.1)
        # return

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_to_elfin())
    loop.close()
    mqtt_client.loop_stop()

if __name__ == '__main__':
    with open(config_dir + '/options.json') as file:
        CONFIG = json.load(file)
    with open(share_dir + '/evill_devinfo.json') as file:
        log('Found device data: /share/ezvill_devinfo.json')
        OPTION = json.load(file)
    while True:
        do_work(CONFIG, OPTION)
