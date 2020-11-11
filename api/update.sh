#!/bin/bash

if [ "$1" == "device" ]
then
  cd /home/pi/device
elif [ "$1" == "client" ]
then
  cd /home/pi/device/api/static
elif [ "$1" == "api" ]
then
  cd /home/pi/device/api
else
  echo "Not a valid upgrade target"
  exit 1
fi
pwd
/usr/bin/git pull origin master 2>&1
