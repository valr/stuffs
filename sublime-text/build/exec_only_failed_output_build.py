import importlib

# the default exec target is defined in exec.py
default_exec = importlib.import_module("Default.exec")


class ExecOnlyFailedOutputBuildCommand(default_exec.ExecCommand):
    def on_finished(self, proc):
        super().on_finished(proc)

        # auto-hide the build output panel on successful build
        exit_code = proc.exit_code()
        if (exit_code == 0 or exit_code is None) and not self.output_view.find_all_results():
            self.window.run_command("hide_panel", {"panel": "output.exec"})
