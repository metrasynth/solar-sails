import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUiType

from sails.ui import App

UIC_NAME = 'sunvoxsettingswidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_SunVoxSettingsWidget, SunVoxSettingsWidgetBase = loadUiType(UIC_PATH)


class SunVoxSettingsWidget(SunVoxSettingsWidgetBase, Ui_SunVoxSettingsWidget):

    def __init__(self, parent):
        super(SunVoxSettingsWidget, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, ui):
        super(SunVoxSettingsWidget, self).setupUi(ui)
        self.item_model = WorkspacePathsItemModel(self)
        self.workspace_paths_list_view.setModel(self.item_model)

    @pyqtSlot()
    def on_add_button_clicked(self):
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption='Select directory containing SunVox app',
        )
        if path:
            self.item_model.add_path(path)

    @pyqtSlot()
    def on_remove_button_clicked(self):
        for index in self.workspace_paths_list_view.selectedIndexes():
            self.item_model.remove_path_at(index)


class WorkspacePathsItemModel(QStandardItemModel):

    def __init__(self, parent):
        super(WorkspacePathsItemModel, self).__init__(parent)
        self._paths = []
        self._load_settings()

    def add_path(self, path):
        if path not in self._paths:
            self._paths.append(path)
            item = QStandardItem(path)
            self.appendRow(item)
            self._save_settings()

    def remove_path_at(self, index):
        path = index.data()
        self._paths.remove(path)
        self.removeRow(index.row())
        self._save_settings()

    def _load_settings(self):
        App.settings.beginGroup('sunvox')
        paths = App.settings.value('workspace_paths')
        if paths is not None:
            self._paths = paths
            self.clear()
            for path in paths:
                self.appendRow(QStandardItem(path))
        App.settings.endGroup()

    def _save_settings(self):
        App.settings.beginGroup('sunvox')
        App.settings.setValue('workspace_paths', self._paths)
        App.settings.endGroup()
