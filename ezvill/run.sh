#!/bin/sh

PY_DIR=/ezvill2mqtt
PY_FILE="ezvill.py"
DEV_FILE="ezvill_devinfo.json"

# start server
echo "[Info] Start ezvill2mqtt.."

if [ ! -f /share/$DEV_FILE ]; then
   cp $PY_DIR/$DEV_FILE /share/$DEV_FILE
fi   
python -u $PY_DIR/$PY_FILE
