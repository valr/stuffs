import os
import subprocess
from typing import cast

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

        command = project_filename.replace(".sublime-project", ".sublime-onevent")
        syntax = (
            cast(str, view.settings().get("syntax", "None"))
            .replace(".sublime-syntax", "")
            .replace(".tmLanguage", "")
            .split("/")[-1]
        )

        if os.path.isfile(command):
            subprocess.Popen([command, event, syntax, filename], cwd=os.path.dirname(filename))
