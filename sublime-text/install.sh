#!/bin/bash

set -u

SOURCE="/stuffs/sublime-text"
TARGET="$HOME"/.config/sublime-text/Packages

if [[ "$PWD" != *"$SOURCE" ]]; then
    echo "The script must be run from within its directory."
fi

# plugins
for PLUGIN in "MarkdownToHtml" "OpenUrl" "RunCommand" "RunOnEvent" "SwitchPanel"
do
    rm -f "$TARGET/$PLUGIN"
    ln -s "$PWD/plugins/$PLUGIN" "$TARGET/$PLUGIN"
done

# settings
for SETTING in "Default (Linux).sublime-keymap" \
    "Distraction Free.sublime-settings" "LSP.sublime-settings" \
    "Package Control.sublime-settings" "Preferences.sublime-settings" \
    "Terminal.sublime-settings"
do
    rm -f "$TARGET/User/$SETTING"
    ln -s "$PWD/settings/$SETTING" "$TARGET/User/$SETTING"
done

# commands
for COMMAND in "Default.sublime-commands"
do
    rm -f "$TARGET/User/$COMMAND"
    ln -s "$PWD/commands/$COMMAND" "$TARGET/User/$COMMAND"
done

# language syntaxes
for SYNTAX in "Gettext.tmLanguage" "Meson.tmLanguage"
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
