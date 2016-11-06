import os

from PyQt5.uic import loadUiType

UIC_NAME = 'audiosettingswidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_AudioSettingsWidget, AudioSettingsWidgetBase = loadUiType(UIC_PATH)


class AudioSettingsWidget(AudioSettingsWidgetBase, Ui_AudioSettingsWidget):

    def __init__(self, parent):
        super(AudioSettingsWidget, self).__init__(parent)
        self.setupUi(self)
