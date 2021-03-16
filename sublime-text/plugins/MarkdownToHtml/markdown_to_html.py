import os
import threading
import webbrowser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import sublime
import sublime_plugin


class MarkdownToHtml(sublime_plugin.EventListener):
    def __init__(self):
        super(MarkdownToHtml, self).__init__()
        self.lock = threading.Lock()
        self.text = {}

    def on_post_save_async(self, view):
        if not view.settings().get("syntax").endswith("Markdown.sublime-syntax"):
            return

        buff = view.buffer_id()
        if buff not in self.text:
            self.text[buff] = ""

        text = view.substr(sublime.Region(0, view.size()))
        if self.text[buff] == text:
            return

        try:
            self.lock.acquire()

            filename = "/tmp/sublimetext-{}.html".format(buff)
            fileexists = os.path.exists(filename)

            with open(filename, "w") as file:
                file.write(self.html_page(self.html_body(text)))

            if not fileexists:
                webbrowser.get("chromium").open_new_tab("file://" + filename)

            self.text[buff] = text
        finally:
            self.lock.release()

        view.window().status_message("Markdown rendered in HTML")

    def on_close(self, view):
        buff = view.buffer_id()
        if buff in self.text:
            del self.text[buff]

        filename = "/tmp/sublimetext-{}.html".format(buff)
        if os.path.exists(filename):
            os.remove(filename)

    def html_body(self, markdown):
        url = "https://api.github.com/markdown/raw"
        header = {"Content-Type": "text/plain"}
        data = markdown.encode("utf-8")

        try:
            request = Request(url, data, header, method="POST")
            body = urlopen(request).read().decode("utf-8")
        except HTTPError as e:
            body = "HTTP error {}: {}".format(e.code, e.reason)
        except URLError as e:
            body = "URL error: {}".format(e.reason)
        finally:
            return body

    def html_page(self, body):
        head = """
<!DOCTYPE html>
<html>
<head>
  <title>Markdown to HTML</title>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: helvetica, arial, sans-serif; font-size: 16px;
           color: #333; line-height: 1.6; margin: 40px auto; padding: 0 30px;
           box-sizing: border-box; min-width: 200px; max-width: 980px;
           border-style: solid; border-width: 1px; border-color: lightgray; }
    h1, h2, h3 { line-height: 1.2; }
  </style>
</head>
<body>
"""
        script = """
<script>
  var reload = false;

  function focus() {
    if (reload == true) {
      // this seems to trigger the reload with chromium
      window.location.href = window.location.href;
      window.location.reload(true);
    }
  }

  function blur() { reload = true; }
  function click() { window.location.reload(true); }

  window.addEventListener("focus", focus);
  window.addEventListener("blur", blur);
  window.addEventListener("click", click);
</script>
</body>
</html>
"""

        return head + body + script
