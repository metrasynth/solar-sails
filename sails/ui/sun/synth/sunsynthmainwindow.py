import os

from PyQt5.uic import loadUiType

from sails.ui.openers.opener import Opener


UIC_NAME = 'sunsynthmainwindow.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_SunSynthMainWindow, SunSynthMainWindowBase = loadUiType(UIC_PATH)


class SunSynthMainWindow(SunSynthMainWindowBase, Ui_SunSynthMainWindow):

    def __init__(self, filename):
        super(SunSynthMainWindow, self).__init__(None)
        self.filename = filename
        self.setupUi(self)

    def setupUi(self, ui):
        from .sunsynthmainmenubar import SunSynthMainMenuBar
        super(SunSynthMainWindow, self).setupUi(ui)
        self.setMenuBar(SunSynthMainMenuBar(self))

    def closeEvent(self, event):
        Opener.remove_file_window(self.filename)
        event.accept()
