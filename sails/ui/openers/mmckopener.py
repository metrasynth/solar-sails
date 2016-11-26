from PyQt5.QtWidgets import qApp

from .opener import Opener


@Opener.register_opener
class MmckOpener(Opener):

    file_ext = '.mmck'
    file_type_label = 'MetaModule Construction Kit'

    @classmethod
    def main_window(cls, filename):
        if not hasattr(qApp, '_tools_mmck'):
            from sails.ui.mmck.mainwindow import MmckMainWindow
            qApp._tools_mmck = MmckMainWindow()
        mmck = qApp._tools_mmck
        mmck.show()
        mmck.setFocus(True)
        with open(filename, 'r') as f:
            data = f.read()
        mmck.main_widget.load_json(data)
        return mmck
