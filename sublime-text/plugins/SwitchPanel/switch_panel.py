import sublime
import sublime_plugin


class SwitchPanel(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("SwitchPanel.sublime-settings")
        ignored_panels = settings.get("ignored_panels", [])

        panels = [
            panel
            for panel in sorted(self.window.panels())
            if panel not in ignored_panels and not self.is_empty(panel)
        ]

        active_panel = self.window.active_panel()

        index_panel = panels.index(active_panel) if active_panel in panels else -1
        index_panel = (index_panel + 1) % len(panels)

        self.window.run_command("show_panel", {"panel": panels[index_panel]})
        self.window.status_message("Switched to panel: " + panels[index_panel])

    def is_empty(self, panel):
        view = self.window.find_output_panel(panel.lstrip("output."))

        if view is not None:
            return not view.substr(sublime.Region(0, view.size())).strip()

        return False
