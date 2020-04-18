#!/bin/sh

PY_DIR=/ezvill2mqtt
PY_FILE="ezvill.py"
DEV_FILE="ezvill_devinfo.json"

# start server
echo "[Info] Start ezvill2mqtt.."

python -u $PY_DIR/$PY_FILE
