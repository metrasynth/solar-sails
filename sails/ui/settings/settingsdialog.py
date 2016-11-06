import os
import sys

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.uic import loadUiType

from sails.ui.settings.audiosettingswidget import AudioSettingsWidget
from sails.ui.settings.sunvoxsettingswidget import SunVoxSettingsWidget

UIC_NAME = 'settingsdialog.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_SettingsDialog, SettingsDialogBase = loadUiType(UIC_PATH)


class SettingsDialog(SettingsDialogBase, Ui_SettingsDialog):

    _global_dialog = None

    def __new__(cls, *args, **kwargs):
        if cls._global_dialog is None:
            dialog = SettingsDialogBase.__new__(cls, *args, **kwargs)
            cls._global_dialog = dialog
        else:
            dialog = cls._global_dialog
        return dialog

    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, ui):
        super(SettingsDialog, self).setupUi(ui)
        if sys.platform == 'darwin':
            self.setWindowTitle('Solar Sails Preferences')
        else:
            self.setWindowTitle('Solar Sails Settings')
        layout = QVBoxLayout(self.audio_tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(AudioSettingsWidget(self.audio_tab))
        layout = QVBoxLayout(self.sunvox_tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(SunVoxSettingsWidget(self.sunvox_tab))
