import html
import re

import sublime
import sublime_plugin


class OpenUrlOnClick(sublime_plugin.ViewEventListener):
    regex = "\\bhttps?://[-A-Za-z0-9+&@#/%?=~_()|!:,.;']*[-A-Za-z0-9+&@#/%=~_(|]"
    html = '<a href="url"><i>Open:</i> <u style="color:white;">url</u></a>'

    def on_hover(self, point, hover_zone):
        if hover_zone != sublime.HOVER_TEXT:
            return

        x = self.view.rowcol(point)[1]
        line = self.view.substr(self.view.line(point))

        content = ""
        for url in re.finditer(self.regex, line):
            if x >= url.start() and x <= url.end():
                content = self.html.replace("url", html.escape(url.group()))

        if content:
            # doc: https://forum.sublimetext.com/t/dev-build-3070/14538
            self.view.show_popup(content, sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                                 point, 4096, on_navigate=self.clicked_url)

    def clicked_url(self, url):
        sublime.run_command("open_url", {"url": url})


class OpenUrlOnSelectionCommand(sublime_plugin.WindowCommand):
    def run(self):
        settings = sublime.load_settings("OpenUrl.sublime-settings")
        items = settings.get("url_list", [])

        self.window.show_quick_panel(
            items, lambda id: self.on_done(id, items),
            sublime.KEEP_OPEN_ON_FOCUS_LOST)

    def on_done(self, id, items):
        if id >= 0:
            sublime.run_command("open_url", {"url": items[id][1]})
