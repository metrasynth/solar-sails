import os

from arrow import now
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUiType
import rv.api as rv
from sails.ui.mmck.mainmenubar import MmckMainMenuBar
from sails.ui.mmck.mainwidget import MmckMainWidget
from sails.ui.openers.mmckopener import MmckOpener

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
        self.setup_menus()

    def setup_menus(self):
        menubar = self.menuBar()
        for action in [
            self.main_widget.action_compile_parameters,
            self.main_widget.action_compile_project,
        ]:
            menubar.code_menu.addAction(action)
        sep = menubar.file_menu.insertSeparator(menubar.file_settings)
        for action in [
            self.action_save,
            self.action_save_as,
            self.action_export_metamodule,
            self.action_export_project,
        ]:
            menubar.file_menu.insertAction(sep, action)

    @pyqtSlot()
    def on_action_export_metamodule_triggered(self):
        path = self.windowFilePath()
        if path:
            mod = rv.m.MetaModule(project=self.main_widget.kit.project)
            synth = rv.Synth(mod)
            timestamp = now().strftime('%Y%m%d%H%M%S')
            filename = '{}-{}.sunsynth'.format(path, timestamp)
            with open(filename, 'wb') as f:
                synth.write_to(f)

    @pyqtSlot()
    def on_action_export_project_triggered(self):
        path = self.windowFilePath()
        if path:
            project = self.main_widget.kit.project
            timestamp = now().strftime('%Y%m%d%H%M%S')
            filename = '{}-{}.sunvox'.format(path, timestamp)
            with open(filename, 'wb') as f:
                project.write_to(f)

    @pyqtSlot()
    def on_action_save_triggered(self):
        path = self.windowFilePath()
        if not path:
            self.on_action_save_as_triggered()
        else:
            with open(path, 'w') as f:
                f.write(self.main_widget.kit.to_json())

    @pyqtSlot()
    def on_action_save_as_triggered(self):
        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save MMCK file',
            directory='.',
            filter=MmckOpener.filter(),
        )
        if path:
            self.setWindowFilePath(path)
            self.on_action_save_triggered()

