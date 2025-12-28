from dataclasses import dataclass
from typing import List

import sublime
import sublime_plugin


@dataclass
class Settings:
    ignored_panels: List[str]


class SwitchPanel(sublime_plugin.WindowCommand):
    def run(self):
        settings = Settings(**sublime.load_settings("SwitchPanel.sublime-settings").to_dict())

        panels = [
            panel
            for panel in sorted(self.window.panels())
            if panel not in settings.ignored_panels and not self.is_empty(panel)
        ]

        active_panel = self.window.active_panel()

        index_panel = panels.index(active_panel) if active_panel in panels else -1
        index_panel = (index_panel + 1) % len(panels)

        self.window.run_command("show_panel", {"panel": panels[index_panel]})
        self.window.status_message("Switched to panel: " + panels[index_panel])

    def is_empty(self, panel: str) -> bool:
        prefix = "output."
        output_panel = panel[len(prefix) :] if panel.startswith(prefix) else panel

        view = self.window.find_output_panel(output_panel)
        if view:
            return not view.substr(sublime.Region(0, view.size())).strip()

        return False
