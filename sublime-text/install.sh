#!/bin/bash

set -u

SOURCE="/stuffs/sublime-text"
TARGET="$HOME"/.config/sublime-text/Packages

if [[ "$PWD" != *"$SOURCE" ]]; then
  echo "The script must be run from within its directory."
fi

# plugins
for PLUGIN in "MarkdownToHtml" \
  "OpenUrlPanel" \
  "RunCommand" \
  "RunOnEvent" \
  "SwitchPanel"
do
  rm -f "$TARGET/$PLUGIN"
  ln -s "$PWD/plugins/$PLUGIN" "$TARGET/$PLUGIN"
done

# settings
for SETTING in "Default (Linux).sublime-keymap" \
  "Default.sublime-commands" \
  "Distraction Free.sublime-settings" \
  "LSP.sublime-settings" \
  "LSP-pylsp.sublime-settings" \
  "PackageDev.sublime-settings" \
  "Package Control.sublime-settings" \
  "Preferences.sublime-settings" \
  "SublimeLinter.sublime-settings" \
  "Terminal.sublime-settings"
do
  rm -f "$TARGET/User/$SETTING"
  ln -s "$PWD/settings/$SETTING" "$TARGET/User/$SETTING"
done

# language syntaxes
for SYNTAX in "Gettext.tmLanguage" \
  "Jinja.sublime-syntax" \
  "Just.sublime-syntax" \
  "Meson.tmLanguage"
do
  rm -f "$TARGET/User/$SYNTAX"
  ln -s "$PWD/syntax/$SYNTAX" "$TARGET/User/$SYNTAX"
done

# builds
for BUILD in "exec_only_failed_output_build.py"
do
  rm -f "$TARGET/User/$BUILD"
  ln -s "$PWD/build/$BUILD" "$TARGET/User/$BUILD"
done
