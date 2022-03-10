from PyQt6.QtWidgets import QApplication

from .opener import Opener


@Opener.register_opener
class MmckOpener(Opener):

    file_ext = ".mmck.py"
    file_type_label = "MetaModule Construction Kit"

    @classmethod
    def main_window(cls, filename):
        qApp = QApplication.instance()
        if not hasattr(qApp, "_tools_mmck"):
            from sails.ui.mmck.mainwindow import MmckMainWindow

            qApp._tools_mmck = MmckMainWindow()
        mmck = qApp._tools_mmck
        mmck.showMaximized()
        mmck.setFocus()
        mmck.load_file(filename)
        return mmck
