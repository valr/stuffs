#!/bin/bash

ACPI=$(acpi -ab | sed 's/Battery 0: //;s/,/:/;s/,/\nRemaining:/;s/ remaining//;s/Adapter 0/AC/')

notify-send -u normal -t 3000 -a battery "${ACPI}"
