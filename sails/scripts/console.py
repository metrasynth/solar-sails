import begin
from jupyter_console.app import launch_new_instance
from jupyter_console.ptshell import ZMQTerminalInteractiveShell


def launch_console():
    launch_new_instance(['--existing'])


def patch_keepserver():
    orig_interact = ZMQTerminalInteractiveShell.interact

    def interact(self, display_banner=None):
        self.keepkernel = True
        return orig_interact(self, display_banner)

    ZMQTerminalInteractiveShell.interact = interact


@begin.start
def main():
    """Open an IPython console with a sailsd engine."""
    patch_keepserver()
    launch_console()
