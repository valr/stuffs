import os
import re
import subprocess

import sublime_plugin


class RunOnEvent(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        self.run_command(view, 'on_post_save')

    def run_command(self, view, event):
        filename = view.file_name()
        project_file_name = view.window().project_file_name()

        if not filename or not project_file_name:
            return

        command = re.sub(
            'sublime-project$',
            'sublime-onevent', project_file_name)

        syntax = view.settings().get('syntax', 'None') \
            .replace('.sublime-syntax', '').replace('.tmLanguage', '') \
            .split('/')[-1]

        if os.path.isfile(command):
            subprocess.Popen(
                [command, event, syntax, filename],
                cwd=os.path.dirname(filename))
