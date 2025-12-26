from typing import Dict, List, Optional, cast

import sublime
import sublime_plugin

UrlSettings = Dict[str, List[List[str]]]
ProjectSettings = Dict[str, UrlSettings]
ProjectData = Dict[str, ProjectSettings]


class OpenUrlPanelCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("OpenUrlPanel.sublime-settings")
        url_list = cast(List[List[str]], settings.get("url_list", []))
        url_list.extend(cast(List[List[str]], settings.get("extend_url_list", [])))
        sort = cast(bool, settings.get("sort", True))

        project_data = cast(Optional[ProjectData], self.window.project_data())
        if project_data:
            settings = project_data.get("settings", {}).get("open_url_panel", {})
            url_list = settings.get("url_list", url_list)
            url_list.extend(settings.get("extend_url_list", []))
            sort = settings.get("sort", sort)

        if sort:
            url_list = sorted(url_list, key=lambda x: x[0])

        self.window.show_quick_panel(
            url_list,
            lambda index: self.on_select(index, url_list),
            sublime.KEEP_OPEN_ON_FOCUS_LOST,
        )

    def on_select(self, index: int, url_list: List[List[str]]) -> None:
        if index >= 0:
            sublime.run_command("open_url", {"url": url_list[index][1]})
