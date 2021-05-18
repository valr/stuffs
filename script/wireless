#!/bin/bash

if [ $(id -u) != 0 ]; then
  echo "this script should be run as root."
  exit 1
fi

WIRELESS="wlp3s0"

killall dhcpcd
killall wpa_supplicant
rm -f /run/wpa_supplicant.pid

ip link set "${WIRELESS}" down
sleep 1

ip link set "${WIRELESS}" up
sleep 1

wpa_supplicant -B -P /run/wpa_supplicant.pid -c /etc/wpa_supplicant/wpa_supplicant.conf -i "${WIRELESS}"
sleep 1

dhcpcd "${WIRELESS}"
