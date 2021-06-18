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
<html lang="en">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/4.0.0/github-markdown.min.css"
    integrity="sha512-Oy18vBnbSJkXTndr2n6lDMO5NN31UljR8e/ICzVPrGpSud4Gkckb8yUpqhKuUNoE+o9gAb4O/rAxxw1ojyUVzg=="
    crossorigin="anonymous" />
  <title>Markdown to HTML</title>
  <style>
    .markdown-body {
      box-sizing: border-box;
      margin: 0 auto;
      max-width: 980px;
      min-width: 200px;
      padding: 45px;
    }

    @media (max-width: 767px) {
      .markdown-body {
        padding: 15px;
      }
    }
  </style>
</head>

<body>
  <article class="markdown-body">
"""

        tail = """
  </article>
  <script>
    var reload = false;

    function focus() {
      if (reload == true) {
        // this seems to trigger the reload with chromium
        window.location.href = window.location.href;
        window.location.reload(true);
      }
    }

    function blur() {
      reload = true;
    }
    function click() {
      window.location.reload(true);
    }

    window.addEventListener("focus", focus);
    window.addEventListener("blur", blur);
    window.addEventListener("click", click);
  </script>
</body>

</html>
"""

        return head + body + tail
