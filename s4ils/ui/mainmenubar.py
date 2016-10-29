from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import qApp, QMenu, QAction, QMenuBar


class MainMenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_actions()
        self.create_menus()

    def create_actions(self):
        self.file_exit = QAction(
            'E&xit', self, triggered=self.on_file_exit_triggered)

    def create_menus(self):
        self.file_menu = self.addMenu('&File')
        self.file_menu.addAction(self.file_exit)

    @pyqtSlot()
    def on_file_exit_triggered(self):
        qApp.quit()
