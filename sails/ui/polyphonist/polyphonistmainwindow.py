import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUiType

from sails.ui import App
from sails.ui.polyphonist.polyphonistmainmenubar import PolyphonistMainMenuBar
from sf.polyphonist import ModulePolyphonist, PatternPolyphonist

UIC_NAME = 'polyphonistmainwindow.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_PolyphonistMainWindow, PolyphonistMainWindowBase = loadUiType(UIC_PATH)


class PolyphonistMainWindow(PolyphonistMainWindowBase,
                            Ui_PolyphonistMainWindow):

    def __init__(self):
        super(PolyphonistMainWindow, self).__init__(None)
        self.setupUi(self)

    @property
    def module_clipboard_path(self):
        return os.path.join(self.workspace_path, '.sunvox_clipboard.sunsynth')

    @property
    def pattern_clipboard_path(self):
        return os.path.join(self.workspace_path, '.sunvox_clipboard.sunpats')

    @property
    def workspace_path(self):
        return self.workspace_path_combobox.currentText()

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
        self.sync_pattern_polyphonist()
        mp = self.module_polyphonist
        pp = self.pattern_polyphonist
        already_poly = mp and mp.module.name.endswith('x)')
        self.polyphonize_module_button.setEnabled(not already_poly)
        self.polyphonize_pattern_button.setEnabled(
            pp and pp.pattern_count and pp.is_compatible)
        self.sync_monophonic_module_combobox()

    def sync_module_polyphonist(self):
        path = self.module_clipboard_path
        label = self.module_clipboard_label
        if os.path.exists(path):
            p = self.module_polyphonist = ModulePolyphonist(path)
            label.setText(repr(p.module))
        else:
            self.module_polyphonist = None
            label.setText('(nothing found in clipboard)')

    def sync_monophonic_module_combobox(self):
        combo_box = self.monophonic_module_combobox
        current = combo_box.currentText()
        combo_box.clear()
        if self.pattern_polyphonist:
            combo_box.setEnabled(True)
            items = [
                '{:02x}'.format(m) for m in
                self.pattern_polyphonist.module_numbers
            ]
            combo_box.addItems(items)
            if current in items:
                combo_box.setCurrentIndex(items.index(current))
        else:
            combo_box.setEnabled(False)

    def sync_pattern_polyphonist(self):
        path = self.pattern_clipboard_path
        label = self.pattern_clipboard_label
        if os.path.exists(path):
            p = self.pattern_polyphonist = PatternPolyphonist(path)
            if p.pattern_count == 0:
                pattern_info = '0 patterns'
            else:
                pattern_info = '{} pattern{}, {}polyphonist compatible'.format(
                    p.pattern_count,
                    's' if p.pattern_count != 1 else '',
                    '' if p.is_compatible else 'not ',
                )
            label.setText(pattern_info)
        else:
            self.pattern_polyphonist = None
            label.setText('(nothing found in clipboard)')

    def sync_project_paths(self):
        workspace_paths = App.settings.value('sunvox/workspace_paths')
        self.workspace_path_combobox.clear()
        self.workspace_path_combobox.addItems(workspace_paths)

    @pyqtSlot(int)
    def on_min_voice_spinbox_valueChanged(self, value):
        self.max_voice_spinbox.setMinimum(value)

    @pyqtSlot()
    def on_polyphonize_module_button_clicked(self):
        voices = self.voice_count_spinbox.value()
        synth = self.module_polyphonist.polyphonized_synth(voices)
        with open(self.module_clipboard_path, 'wb') as f:
            synth.write_to(f)
        self.sync_all()

    @pyqtSlot()
    def on_polyphonize_pattern_button_clicked(self):
        mono_module = int(self.monophonic_module_combobox.currentText(), 16)
        poly_module = int(self.polyphonic_module_lineedit.text(), 16)
        min_voice = self.min_voice_spinbox.value()
        max_voice = self.max_voice_spinbox.value()
        poly_project = self.pattern_polyphonist.polyphonized_project(
            mono_module=mono_module,
            poly_module=poly_module,
            min_voice=min_voice,
            max_voice=max_voice,
        )
        with open(self.pattern_clipboard_path, 'wb') as f:
            poly_project.write_to(f)
        self.sync_all()

    @pyqtSlot(int)
    def on_voice_count_spinbox_valueChanged(self, value):
        self.min_voice_spinbox.setMaximum(value)
        self.max_voice_spinbox.setMaximum(value)
        self.max_voice_spinbox.setValue(value)
