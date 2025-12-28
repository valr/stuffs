import os
import subprocess

import sublime
import sublime_plugin


class RunOnEvent(sublime_plugin.EventListener):
    def on_post_save_async(self, view: sublime.View) -> None:
        self.run_command(view, "on_post_save")

    def run_command(self, view: sublime.View, event_name: str) -> None:
        window = view.window()
        project_file_name = window.project_file_name() if window else None
        if not project_file_name:
            return

        file_name = view.file_name()
        if not file_name:
            return

        syntax = view.syntax()
        syntax_name = syntax.name if syntax else "None"

        command = project_file_name.replace(".sublime-project", ".sublime-onevent")
        if os.path.isfile(command):
            subprocess.Popen([command, event_name, syntax_name, file_name], cwd=os.path.dirname(file_name))
