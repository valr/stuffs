#!/bin/bash

# change brightness using xbacklight

case "$1" in
  [0-9]*) xbacklight -set "$1" ;;
  +) xbacklight -inc 5 ;;
  -) xbacklight -dec 5 ;;
  *) exit 1 ;;
esac

PERCENT="$(xbacklight -get | cut -d'.' -f1)"

notify-send -u normal -t 1000 -a brightness "luminosité: ${PERCENT}%"
