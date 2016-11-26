import os

from PyQt5.QtCore import QStringListModel, pyqtSlot
from PyQt5.uic import loadUiType
from sails.lib import mido
from sails import midi
from sails.ui import App

UIC_NAME = 'midisettingswidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_MidiSettingsWidget, MidiSettingsWidgetBase = loadUiType(UIC_PATH)


class MidiSettingsWidget(MidiSettingsWidgetBase, Ui_MidiSettingsWidget):

    def __init__(self, parent):
        super(MidiSettingsWidget, self).__init__(parent)
        self.setupUi(self)
        self.setup_model()

    def setupUi(self, ui):
        super().setupUi(ui)

    def setup_model(self):
        self.midi_in_model = QStringListModel()
        self.midi_in_model.setStringList(mido.backend.get_input_names())
        self.midi_in_listview.setModel(self.midi_in_model)
        self.midi_in_listview.selectionModel().selectionChanged.connect(
            self.on_midi_in_selection_changed)
        self.load_midi_in_selection()

    @property
    def midi_in_selected(self):
        return set(
            self.midi_in_model.data(i, 0)
            for i in self.midi_in_listview.selectedIndexes()
        )

    @midi_in_selected.setter
    def midi_in_selected(self, value):
        model = self.midi_in_model
        selection = self.midi_in_listview.selectionModel()
        selection.clear()
        for i in range(model.rowCount()):
            i = model.index(i, 0)
            data = model.data(i, 0)
            if data in value:
                selection.select(i, selection.Select)

    @property
    def midi_in_unselected(self):
        return set(self.midi_in_model.stringList()) - self.midi_in_selected

    def load_midi_in_selection(self):
        App.settings.beginGroup('midi')
        try:
            paths = App.settings.value('in_devices')
            paths = set(paths) if paths is not None else set()
            self.midi_in_selected = paths
        finally:
            App.settings.endGroup()

    def save_midi_in_seletion(self):
        App.settings.beginGroup('midi')
        try:
            paths = App.settings.value('in_devices')
            paths = set(paths) if paths is not None else set()
            paths.update(self.midi_in_selected)
            paths -= self.midi_in_unselected
            App.settings.setValue('in_devices', list(sorted(paths)))
        finally:
            App.settings.endGroup()
        midi.listener.update_ports()

    @pyqtSlot()
    def on_midi_in_refresh_button_clicked(self):
        self.setup_model()

    @pyqtSlot()
    def on_midi_in_selection_changed(self):
        self.save_midi_in_seletion()
