import os
import sys
from PyQt6.uic import loadUiType

import py

UIC_NAME = 'welcomewidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_WelcomeWidget, WelcomeWidgetBase = loadUiType(UIC_PATH)


def solar_sails_version():
    version_txt = py.path.local(sys.argv[0]).dirpath() / 'solar-sails-version.txt'
    if version_txt.isfile():
        return version_txt.read('rU').strip()


class WelcomeWidget(WelcomeWidgetBase, Ui_WelcomeWidget):

    def __init__(self, parent):
        super(WelcomeWidget, self).__init__(parent)
        self.setupUi(self)
        version = solar_sails_version()
        if version is not None:
            self.buildLabel.setText(version)
