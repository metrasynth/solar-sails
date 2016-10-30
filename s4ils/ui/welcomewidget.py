import os
from PyQt5.uic import loadUiType

UIC_NAME = 'welcomewidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_WelcomeWidget, WelcomeWidgetBase = loadUiType(UIC_PATH)


class WelcomeWidget(WelcomeWidgetBase, Ui_WelcomeWidget):

    def __init__(self, parent):
        super(WelcomeWidget, self).__init__(parent)
        self.setupUi(self)
