import sublime
import sublime_plugin


class OpenUrlPanelCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("OpenUrlPanel.sublime-settings")
        items = settings.get("url_list", [])

        self.window.show_quick_panel(
            items, lambda id: self.on_done(id, items), sublime.KEEP_OPEN_ON_FOCUS_LOST
        )

    def on_done(self, id, items):
        if id >= 0:
            sublime.run_command("open_url", {"url": items[id][1]})
