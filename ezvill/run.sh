#!/bin/sh

PY_DIR=/ezvill2mqtt
PY_FILE="ezvill.py"
DEV_FILE="ezvill_devinfo.json"

# start server
echo "[Info] Start ezvill2mqtt.."

cp $PY_DIR/$DEV_FILE /share/$DEV_FILE
python -u $PY_DIR/$PY_FILE
