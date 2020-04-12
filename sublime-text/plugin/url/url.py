import re
import subprocess
# import webbrowser

import sublime
import sublime_plugin


class Url(sublime_plugin.ViewEventListener):
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
                content = self.html.replace('url', url.group())

        if content:
            # doc: https://forum.sublimetext.com/t/dev-build-3070/14538
            self.view.show_popup(content, sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                                 point, on_navigate=self.url_clicked)

    def url_clicked(self, url):
        # For some reason open_new_tab fails (well, firefox fails to start)
        # when there is no running instance of firefox. Replacing by xdg-open.
        #webbrowser.open_new_tab(self.url)
        subprocess.Popen('xdg-open ' + url, shell=True)
