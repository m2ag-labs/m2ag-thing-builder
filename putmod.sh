#!/usr/bin/env bash
# TODO: update host name
echo "copy $1 to config, $2 to thing"
cp "config/available/components/$1.json" "../m2ag-things/components/$1/$1.json"
cp "device/hardware/components/$1.py" "../m2ag-things/components/$1/$1.py"
cp "config/available/things/$2.json" "../m2ag-things/things/$2/$2.json"
cp "device/things/$2.py" "../m2ag-things/things/$2/$2.py"
