import os

from PyQt5.uic import loadUiType
from sails.ui.mmck.mainmenubar import MmckMainMenuBar
from sails.ui.mmck.mainwidget import MmckMainWidget

UIC_NAME = 'mainwindow.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_MmckMainWindow, MmckMainWindowBase = loadUiType(UIC_PATH)


class MmckMainWindow(MmckMainWindowBase, Ui_MmckMainWindow):

    def __init__(self):
        super(MmckMainWindow, self).__init__(None)
        self.setupUi(self)

    def setupUi(self, ui):
        super(MmckMainWindow, self).setupUi(ui)
        self.setMenuBar(MmckMainMenuBar())
        self.main_widget = MmckMainWidget(self)
        self.scroll_area.setWidget(self.main_widget)
