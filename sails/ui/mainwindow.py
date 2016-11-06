import os
from PyQt5.uic import loadUiType

UIC_NAME = 'mainwindow.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_MainWindow, MainWindowBase = loadUiType(UIC_PATH)


class MainWindow(MainWindowBase, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.setupUi(self)
