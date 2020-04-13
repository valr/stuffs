import sublime
import sublime_plugin


# test: window.run_command('panel_switch')

class PanelSwitch(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("PanelSwitch.sublime-settings")
        ignored_panels = settings.get("ignored_panels", [])

        panels = sorted(self.window.panels())
        panels = [panel for panel in panels if panel not in ignored_panels]

        active_panel = self.window.active_panel()

        index_panel = panels.index(active_panel) if active_panel in panels else -1
        index_panel = (index_panel + 1) % len(panels)

        self.window.run_command("show_panel", {"panel": panels[index_panel]})
        self.window.status_message("Switched to panel: " + panels[index_panel])
