from dataclasses import dataclass, replace
from typing import Dict, List, Optional, cast

import sublime
import sublime_plugin


@dataclass
class GlobalSettings:
    sort: bool
    url_list: List[List[str]]
    extend_url_list: List[List[str]]


@dataclass
class ProjectSettings:
    sort: Optional[bool] = None
    url_list: Optional[List[List[str]]] = None
    extend_url_list: Optional[List[List[str]]] = None


class OpenUrlPanelCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = GlobalSettings(**sublime.load_settings("OpenUrlPanel.sublime-settings").to_dict())

        project_data = cast(Dict, self.window.project_data())
        if project_data:
            project_settings = ProjectSettings(**project_data.get("settings", {}).get("open_url_panel", {}))
            settings = replace(settings, **{k: v for k, v in vars(project_settings).items() if v is not None})

        url_list = settings.url_list + settings.extend_url_list
        if settings.sort:
            url_list = sorted(url_list, key=lambda x: x[0])

        self.window.show_quick_panel(
            url_list,
            lambda index: self.on_select(index, url_list),
            sublime.KEEP_OPEN_ON_FOCUS_LOST,
        )

    def on_select(self, index: int, url_list: List[List[str]]) -> None:
        if index >= 0:
            sublime.run_command("open_url", {"url": url_list[index][1]})
