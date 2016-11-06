import os

from PyQt5.uic import loadUiType

from sails.ui.openers.opener import Opener


UIC_NAME = 'sunvoxmainwindow.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_SunVoxMainWindow, SunVoxMainWindowBase = loadUiType(UIC_PATH)


class SunVoxMainWindow(SunVoxMainWindowBase, Ui_SunVoxMainWindow):

    def __init__(self, filename):
        super(SunVoxMainWindow, self).__init__(None)
        self.filename = filename
        self.setupUi(self)

    def setupUi(self, ui):
        from .sunvoxmainmenubar import SunVoxMainMenuBar
        super(SunVoxMainWindow, self).setupUi(ui)
        self.setMenuBar(SunVoxMainMenuBar(self))

    def closeEvent(self, event):
        Opener.remove_file_window(self.filename)
        event.accept()
