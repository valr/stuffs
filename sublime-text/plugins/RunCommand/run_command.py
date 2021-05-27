import re
import subprocess

import sublime
import sublime_plugin


class ArgumentInputHandler(sublime_plugin.TextInputHandler):
    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments

    def name(self):
        return self.arguments[0]

    def placeholder(self):
        # format of arguments: ${arg_xxx} or ${arg_xxx|yyy}
        # arg_xxx = argument name
        # yyy = argument default value (optional)
        try:
            return self.arguments[0][6:self.arguments[0].rindex("|")]
        except ValueError:
            return self.arguments[0][6:-1]

    def initial_text(self):
        try:
            return self.arguments[0][self.arguments[0].rindex("|") + 1:-1]
        except ValueError:
            return ""

    def preview(self, text):
        return self.command.replace(self.arguments[0], text) if text else self.command

    def confirm(self, text):
        self.value = text

    def next_input(self, args):
        return ArgumentInputHandler(
            self.command.replace(self.arguments[0], self.value),
            self.arguments[1:]) if len(self.arguments) > 1 else None


class CommandInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self):
        return "command"

    def next_input(self, args):
        command, arguments = CommandInputHandler.get_command_arguments(args)
        return ArgumentInputHandler(command, arguments) if arguments else None

    @staticmethod
    def get_command_arguments(args):
        command = args["command"]
        return command, re.findall(r"\$\{arg_.+?\}", command)


class RunCommandCommand(sublime_plugin.TextCommand):
    def input(self, args):
        if "command" not in args:
            return CommandInputHandler()
        else:
            command, arguments = CommandInputHandler.get_command_arguments(args)
            return ArgumentInputHandler(command, arguments) if arguments else None

    def run(self, edit, **kwargs):
        # command to execute
        # mandatory, if not provided in .sublime-commands it will be provided via the input handler
        command = kwargs.get("command")

        # replace the command arguments in format ${arg_xxx} or ${arg_xxx|yyy}
        # by the corresponding value provided via the input handler
        for key, value in kwargs.items():
            if key[:6] + key[-1:] == "${arg_}":
                command = command.replace(key, value)

        # working directory where the command will be executed
        # optional, values: "a_path", "$a_variable"
        # (variables are the ones accepted by the extract_variables function
        # defined in https://www.sublimetext.com/docs/3/api_reference.html)
        cwd = kwargs.get("cwd", None)
        if cwd and len(cwd) > 0 and cwd[0] == "$":
            cwd = self.view.window().extract_variables().get(cwd[1:], None)

        # timeout of the command
        # optional, value: number of seconds (default = 30)
        timeout = kwargs.get("timeout", 30)
        if not isinstance(timeout, int):
            timeout = 30

        # target of the command output
        # optional, values: "selection" (default), "window", "none"
        target = kwargs.get("target", "selection")

        # source data passed as command input
        # optional, values: "selection" (default), "window", "none"
        source = kwargs.get("source", "selection")

        if source == "selection":
            regions = self.view.sel()
        elif source == "window":
            regions = [sublime.Region(0, self.view.size())]
        else:
            regions = [None]

        for region in regions:
            self.run_command(command, cwd, timeout, edit, region, target)

    def run_command(self, command, cwd, timeout, edit, region, target):
        try:
            process = subprocess.Popen(
                command, bufsize=-1, cwd=cwd, shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            stdin = self.view.substr(region).encode("utf-8") if region else b""
            stdout, stderr = process.communicate(stdin, timeout)
        except subprocess.TimeoutExpired as err:
            process.kill()
            process.communicate()
            sublime.error_message(str(err))
            return
        except subprocess.SubprocessError as err:
            sublime.error_message(str(err))
            return

        if stderr:
            sublime.error_message(stderr.decode("utf-8"))
            return

        if target == "selection" and region is not None:
            if stdin != stdout:
                self.view.replace(edit, region, stdout.decode("utf-8"))
        elif target == "window":
            view = self.view.window().new_file()
            view.set_name(command)
            view.set_scratch(True)
            view.run_command("append", {"characters": stdout.decode("utf-8")})

        self.view.window().status_message(command)
