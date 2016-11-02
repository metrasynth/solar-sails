import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import qApp, QAction, QMenuBar

from s4ils.ui.openers.sunvoxopener import SunvoxOpener
from s4ils.ui.settings.settingsdialog import SettingsDialog


class MainMenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_actions()
        self.create_menus()

    def create_actions(self):
        self.file_open_sunvox = QAction(
            'Open Sun&Vox file...', self,
            triggered=self.on_file_open_sunvox_triggered)
        self.file_settings = QAction(
            'Se&ttings...', self,
            triggered=self.on_file_settings_triggered)
        self.file_exit = QAction(
            'E&xit', self,
            triggered=self.on_file_exit_triggered)
        self.tools_polyphonist = QAction(
            'Solar Flares &Polyphonist...', self,
            triggered=self.on_tools_polyphonist_triggered)

    def create_menus(self):
        self.file_menu = self.addMenu('&File')
        self.file_menu.addAction(self.file_open_sunvox)
        self.file_menu.addAction(self.file_settings)
        self.file_menu.addAction(self.file_exit)
        self.tools_menu = self.addMenu('&Tools')
        self.tools_menu.addAction(self.tools_polyphonist)

    @pyqtSlot()
    def on_file_exit_triggered(self):
        qApp.quit()

    @pyqtSlot()
    def on_file_open_sunvox_triggered(self):
        opener = SunvoxOpener(self)
        window = opener.exec_()
        if window is not None:
            logging.debug('Got window %r', window)
            window.show()
            window.setFocus(True)

    @pyqtSlot()
    def on_file_settings_triggered(self):
        SettingsDialog(None).show()

    @pyqtSlot()
    def on_tools_polyphonist_triggered(self):
        if not hasattr(qApp, '_tools_polyphonist'):
            from s4ils.ui.polyphonist.polyphonistmainwindow import PolyphonistMainWindow
            qApp._tools_polyphonist = PolyphonistMainWindow()
        qApp._tools_polyphonist.show()
        qApp._tools_polyphonist.setFocus(True)
