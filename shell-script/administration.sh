#!/bin/bash

secure() {
  find /home/valr/document/administration -exec chown root:root '{}' \;
  find /home/valr/document/administration -type d -exec chmod 700 '{}' \;
  find /home/valr/document/administration -type f -exec chmod 600 '{}' \;
}

unsecure() {
  find /home/valr/document/administration -exec chown valr:valr '{}' \;
  find /home/valr/document/administration -type d -exec chmod 755 '{}' \;
  find /home/valr/document/administration -type f -exec chmod 644 '{}' \;
}

case "$1" in
  secure) secure ;;
  unsecure) unsecure ;;
  *) echo "usage: $(basename "$0") {secure|unsecure}" ;;
esac
