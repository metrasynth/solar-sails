import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUiType

from sf.polyphonist import ModulePolyphonist, PatternPolyphonist

from s4ils.ui import App
from s4ils.ui.polyphonist.polyphonistmainmenubar import PolyphonistMainMenuBar

UIC_NAME = 'polyphonistmainwindow.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_PolyphonistMainWindow, PolyphonistMainWindowBase = loadUiType(UIC_PATH)


class PolyphonistMainWindow(PolyphonistMainWindowBase, Ui_PolyphonistMainWindow):

    def __init__(self):
        super(PolyphonistMainWindow, self).__init__(None)
        self.setupUi(self)

    @property
    def module_clipboard_path(self):
        return os.path.join(self.workspace_path, '.sunvox_clipboard.sunsynth')

    @property
    def pattern_clipboard_path(self):
        return os.path.join(self.workspace_path, '.sunvox_clipboard.sunpat')

    @property
    def workspace_path(self):
        return self.workspace_path_combo_box.currentText()

    def focusInEvent(self, event):
        self.sync_all()
        event.accept()

    def setupUi(self, ui):
        super(PolyphonistMainWindow, self).setupUi(ui)
        self.setMenuBar(PolyphonistMainMenuBar())
        self.sync_all()

    def sync_all(self):
        self.sync_project_paths()
        self.sync_module_polyphonist()
        mp = self.module_polyphonist
        already_poly = mp and mp.module.name.endswith('x)')
        self.polyphonize_module_button.setEnabled(not already_poly)

    def sync_module_polyphonist(self):
        if os.path.exists(self.module_clipboard_path):
            self.module_polyphonist = ModulePolyphonist(
                self.module_clipboard_path)
            self.module_clipboard_label.setText(
                repr(self.module_polyphonist.module))
        else:
            self.module_polyphonist = None
            self.module_clipboard_label.setText('(nothing found in clipboard)')

    def sync_project_paths(self):
        workspace_paths = App.settings.value('sunvox/workspace_paths')
        self.workspace_path_combo_box.clear()
        self.workspace_path_combo_box.addItems(workspace_paths)

    @pyqtSlot()
    def on_polyphonize_module_button_clicked(self):
        voices = self.voice_count_spinbox.value()
        synth = self.module_polyphonist.polyphonized_synth(voices)
        with open(self.module_clipboard_path, 'wb') as f:
            synth.write_to(f)
        self.sync_all()

    @pyqtSlot(int)
    def on_voice_count_spinbox_valueChanged(self, value):
        self.min_voice_spinbox.setMaximum(value)
        self.max_voice_spinbox.setMaximum(value)

    @pyqtSlot(int)
    def on_min_voice_spinbox_valueChanged(self, value):
        self.max_voice_spinbox.setMinimum(value)
