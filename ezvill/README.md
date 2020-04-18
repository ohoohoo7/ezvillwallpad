이지빌 월패드용 조명제어 HA 애드온 (EW11의 MQTT통신 사용)
==========================================================
다음의 특징을 가집니다.
1. 사람님의 코맥스월패드용 애드온을 참고로 이지빌에 맞게 수정 (자동으로 기기 찾는기능 삭제하고 전등만 제어가능)
2. elfin ew11에 mqtt 통신 설정을 해야 합니다. (아래 스크린샷 참고)

설치전 준비사항
-----------
1. elfin ew11 설정화면의 'Serial Port Settings'을 다음으로 설정합니다.
![ew11 serial 설정화면](https://github.com/ohoohoo7/ezvillwallpad/blob/master/img/ew11-serial.png)

2. elfin ew11 설정화면의 'Communication Settings'에서 다음을 추가합니다.
![ew11 설정화면](https://github.com/ohoohoo7/ezvillwallpad/blob/master/img/ew11-mqtt.png)

* 설정 저장 후 기기의 재시작이 필요할 수 있습니다.


설치 방법
-------
1. Supervisor -> ADD-ON STORE 이동
2. "https://github.com/ohoohoo7/ezvillwallpad" 를 Repositories 에 추가하고 새로 고침을 합니다.
3. ohoohoo7's Repository 항목으로 이동하여 "EZvill2mqtt"를 선택하고 INSTALL을 눌러 설치합니다.

설정 화면
-------
<pre><code>
"DEBUG": false,
"mqtt_log": true,
"elfin_log": false,
"save_unregistered_signal": false,
"mqtt_server": "192.168.x.x",
"mqtt_id": "id",
"mqtt_password": "pwd"
"data_prefix": "F7"
</code></pre>

#### DEBUG : true / false
작업 내역과 저장된 상태 전부를 출력합니다.
#### mqtt_log : true / false
MQTT 전송 신호를 출력합니다.
#### elfin_log : true / false
ew11을 통해 보내거나 받은 신호를 출력합니다.
#### save_unregistered_signal : true / false
등록되지 않은 신호 20개를 출력하고, /share/collected_signal.txt 에 저장합니다.

#### mqtt_server : 문자
mqtt 서버의 IP 주소를 적습니다. ex) 192.168.0.2
#### mqtt_id : 문자
mqtt 서버 사용자의 아이디를 적습니다.
#### mqtt_password": 문자
mqtt 서버 사용자의 암호를 적습니다. 숫자암호인 경우 꼭 따옴표 "1234"를 해주세요.
#### data_prefix": 문자
이지빌의 조명제어용 HEX코드의 맨 앞글자 2개 입력(표준상 일반적으로 F7)

기기 정보 파일 (ezvill_devinfo.json) 사용법
-------------------------------------------
사람님이 만드신 코맥스용과 다르게 
share 폴더에 기기 정보 파일 ezvill_devinfo.json을 자기집 사정에 맞게 수정해야함

기기 정보 파일 (ezvill_devinfo.json) 예
-----------------------
<pre><code>
{
  "room1": {
    "Number": 1,
    "commandOFF": "F70E124103010000A804",
    "commandON": "F70E124103010100A906",
    "deviceSEPERATOR": "1281",
    "seperatorSTARTNUM" "5",
    "stateOFF": "F70E12810200006802",
    "stateON": "F70E12810200016904"
  },
  "room2": {
    "Number": 1,
    "commandOFF": "F70E134103010000A906",
    "commandON": "F70E134103010100A806",
    "deviceSEPERATOR": "1381",
    "seperatorSTARTNUM" "5",
    "stateOFF": "F70E13810200006904",
    "stateON": "F70E13810200016804"
  },
  "room3": {
    "Number": 1,
    "commandOFF": "F70E144103010000AE0C",
    "commandON": "F70E144103010100AF0E",
    "deviceSEPERATOR": "1481",
    "seperatorSTARTNUM" "5",
    "stateOFF": "F70E14810200006E0A",
    "stateON": "F70E14810200016F0C"
  },
  "room4": {
    "Number": 1,
    "commandOFF": "F70E154103010000AF0E",
    "commandON": "F70E154103010100AE0E",
    "deviceSEPERATOR": "1581",
    "seperatorSTARTNUM" "5",
    "stateOFF": "F70E15810200006F0C",
    "stateON": "F70E15810200016E0C"
  },
  "livingroom1": {
    "Number": 3,
    "commandOFF": "F70E114103010000AB06",
    "commandON": "F70E114103010100AA06",
    "deviceSEPERATOR": "1181",
    "seperatorSTARTNUM" "5",
    "stateNUM1": "14",
    "stateNUM2": "16",
    "stateNUM3": "17",
    "stateOFF": "0",
    "stateON": "1"
  },
  "livingroom2": {
    "Number": 3,
    "commandOFF": "F70E114103020000A804",
    "commandON": "F70E114103020100A906",
    "deviceSEPERATOR": "1181",
    "seperatorSTARTNUM" "5",
    "stateNUM1": "14",
    "stateNUM2": "16",
    "stateNUM3": "17",
    "stateOFF": "0",
    "stateON": "1"
  },
   "livingroom3": {
    "Number": 3,
    "commandOFF": "F70E114103030000A906",
    "commandON": "F70E114103030100A806",
    "deviceSEPERATOR": "1181",
    "seperatorSTARTNUM" "5",
    "stateNUM1": "14",
    "stateNUM2": "16",
    "stateNUM3": "17",
    "stateOFF": "0",
    "stateON": "1"
  }
}
</code></pre>

기기 정보 파일 (ezvill_devinfo.json) 옵션 설명
---------------------------------------------
### 기본 기기 옵션
1. Number : 전등종류 분류 (개별동작등의 경우 1, 거실등과 같이 집합등의 경우 등의 갯수)
 - Number가 #이면 같은이름의 기기항목이 "이름#" 형태로 #개 존재해야하며 "stateNUM#" 항목도 #개 존재해야함 
  예) 기기room의 Number가 3이면 기기명 room1, room2, room3 에 각각 stateNUM1, stateNUM2,stateNUM3 이 존재해야함
2. commandOFF, commandON : 기기를 켜거나 끄는 HEX 코드
3. deviceSEPERATOR : 상태HEX에서 다른기기와 구별되는 시리얼 코드
4. seperatorSTARTNUM : deviceSEPERATOR 가 HEX에서 시작되는 자리수
5. statueNUM# : 집합등의 경우 HEX코드 한개로 여러등의 상태를 나타내므로 집합등의 상태를 나타내주는 HEX코드에서 각등의 상태를 표시해주는 곳의 자리수
 예) 1번등 이 14번째 2번등이 16번째이면 "stateNUM1" : "14", "stateNUM2": "16"
6. stateOFF, stateON : 기기의 상태를 알려주는 HEX 코드 (집합등의 HEX코드 한개로 여러등의 상태를 나타내므로 집합등의 상태를 나타내주는 HEX코드에서 각등의 상태를 표시해주는 곳의 값)


기기 등록 예
------------

<pre><code>

light:
  - platform: mqtt
    name: "거실등1"
    state_topic: "homenet/Light1/power/state"
    command_topic: "homenet/Light1/power/command"
  - platform: mqtt
    name: "거실등2"
    state_topic: "homenet/Light2/power/state"
    command_topic: "homenet/Light2/power/command"

</code></pre>
