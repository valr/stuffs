#!/bin/bash

set -u

SOURCE="/stuffs/sublime-merge"
TARGET="$HOME"/.config/sublime-merge/Packages

if [[ "$PWD" != *"$SOURCE" ]]; then
  echo "The script must be run from within its directory."
fi

# settings
for SETTING in "Commit Message.sublime-settings" \
  "Default (Linux).sublime-keymap" \
  "Diff.sublime-settings" \
  "Preferences.sublime-settings"; do
  rm -f "$TARGET/User/$SETTING"
  ln -s "$PWD/settings/$SETTING" "$TARGET/User/$SETTING"
done
