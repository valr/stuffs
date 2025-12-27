import os
import subprocess

import sublime
import sublime_plugin


class RunOnEvent(sublime_plugin.EventListener):
    def on_post_save_async(self, view: sublime.View) -> None:
        self.run_command(view, "on_post_save")

    def run_command(self, view: sublime.View, event: str) -> None:
        filename = view.file_name()
        project_filename = view.window().project_file_name() if view.window() else None  # type: ignore
        if not filename or not project_filename:
            return

        syntax = view.syntax().name if view.syntax() else "None"  # type: ignore
        command = project_filename.replace(".sublime-project", ".sublime-onevent")
        if os.path.isfile(command):
            subprocess.Popen([command, event, syntax, filename], cwd=os.path.dirname(filename))
