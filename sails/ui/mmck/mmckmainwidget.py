import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUiType

from sails.ui import App

UIC_NAME = 'mmckmainwidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_MmckMainWidget, MmckMainWidgetBase = loadUiType(UIC_PATH)


class MmckMainWidget(MmckMainWidgetBase, Ui_MmckMainWidget):

    def __init__(self, parent=None):
        super(MmckMainWidget, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, ui):
        super(MmckMainWidget, self).setupUi(ui)
