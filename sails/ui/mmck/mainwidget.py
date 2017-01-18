import os
import traceback
from collections import defaultdict
from enum import Enum

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QFrame, qApp
from PyQt5.QtWidgets import QLabel
from PyQt5.uic import loadUiType
from qutepart import Qutepart
from rv.cmidmap import MidiMessageType
from rv.controller import Range

from sails import midi
from sf.mmck.kit import Kit
from sf.mmck.project import Group

from sails.midi.ccmappings import cc_mappings
from sails.ui.outputcatcher import OutputCatcher
from sunvox.api import NOTECMD, Process, Slot

from .project.manager import ControllersManager
from .parameters.manager import ParametersManager

UIC_NAME = 'mainwidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_MmckMainWidget, MmckMainWidgetBase = loadUiType(UIC_PATH)

DEBOUNCE_MSEC = 125
EDITOR_MIN_WIDTH = 500
EMPTY_GROUP = Group()


class MmckMainWidget(MmckMainWidgetBase, Ui_MmckMainWidget):

    def __init__(self, parent=None):
        super(MmckMainWidget, self).__init__(parent)
        self._active_playback_notes = 0
        self.clear_midi_mapping()
        self.clear_udc_list()
        self.kit = Kit()
        self.setupUi(self)

    def setupUi(self, ui):
        super(MmckMainWidget, self).setupUi(ui)
        self.setup_parameter_editor()
        self.setup_parameters()
        self.setup_project_editor()
        self.setup_controllers()
        self.setup_sunvox_process()
        self.setup_sunvox_slot()
        self.setup_midi_routing()
        self.stub4 = QFrame(self)
        self.stub5 = QFrame(self)
        self.layout_4.addWidget(self.stub4)
        self.layout_5.addWidget(self.stub5)
        # noinspection PyCallByClass
        QTimer.singleShot(0, self.setup_parameter_splitter)
        QTimer.singleShot(0, self.setup_project_splitter)
        QTimer.singleShot(0, self.parameter_editor.setFocus)

    def setup_controllers(self):
        self.controllers_manager = ControllersManager(
            parent=self.scrollarea_4,
            layout=self.layout_4,
            root_group=EMPTY_GROUP,
        )
        self.controllers_manager.mapping_changed.connect(
            self.on_controllers_manager_mapping_changed)
        self.controllers_manager.value_changed.connect(
            self.on_controllers_manager_value_changed)
        self.controllers_manager.udc_changed.connect(
            self.on_controllers_manager_udc_changed)

    def setup_midi_routing(self):
        midi.listener.message_received.connect(
            self.on_midi_listener_message_received)

    def setup_parameter_editor(self):
        self.parameter_editor_debouncer = None
        editor = self.parameter_editor = Qutepart(self)
        editor.setMinimumWidth(EDITOR_MIN_WIDTH)
        p = editor.sizePolicy()
        p.setVerticalPolicy(p.Expanding)
        editor.detectSyntax(language='Python')
        editor.textChanged.connect(self.on_parameter_editor_textChanged)
        editor.setPlainText(SAMPLE_PARAMETER_FACTORY)
        self.layout_1.addWidget(editor)

    def setup_parameter_splitter(self):
        splitter = self.parameter_splitter
        splitter.setSizes([sum(splitter.sizes()) - 200, 200])

    def setup_parameters(self):
        self.parameters_manager = ParametersManager(
            parent=self.scrollarea_2,
            layout=self.layout_2,
            parameters={},
            values=self.kit.parameter_values,
        )
        self.parameters_manager.valuesChanged.connect(
            self.on_parameters_manager_valuesChanged)

    def setup_project_editor(self):
        self.project_editor_debouncer = None
        editor = self.project_editor = Qutepart(self)
        editor.setMinimumWidth(EDITOR_MIN_WIDTH)
        p = editor.sizePolicy()
        p.setVerticalPolicy(p.Expanding)
        editor.detectSyntax(language='Python')
        editor.textChanged.connect(self.on_project_editor_textChanged)
        editor.setPlainText(SAMPLE_PROJECT_FACTORY)
        self.layout_3.addWidget(editor)

    def setup_project_splitter(self):
        splitter = self.project_splitter
        splitter.setSizes([sum(splitter.sizes()) - 200, 200])

    def setup_sunvox_process(self):
        self.sunvox = Process()
        self.sunvox.init(None, 44100, 2, 0)
        qApp.aboutToQuit.connect(self.shutdown_sunvox_process)

    def setup_sunvox_slot(self):
        if hasattr(self, 'slot'):
            self.slot.close()
        self.slot = Slot(process=self.sunvox)
        self.slot.volume(256)

    def shutdown_sunvox_process(self):
        self.sunvox.deinit()
        self.sunvox.kill()

    def clear_midi_mapping(self):
        self.controller_aliases = defaultdict(set)
        self.alias_controllers = defaultdict(set)

    def clear_udc_list(self):
        self.udc_list = []

    def clear_udc_widgets(self):
        while self.layout_5.count() > 0:
            child = self.layout_5.takeAt(0)
            w = child.widget()
            if w:
                w.close()
                w.deleteLater()

    def auto_map_controllers(self):
        for alias, (name, w) in zip(cc_mappings.options[1:], self.controllers_manager.controller_widgets.items()):
            try:
                w.set_cc_alias(alias)
            except (SystemError, RuntimeError):
                continue
            mod = w.module
            ctl = w.ctl
            ccs = cc_mappings.alias_ccs[alias]
            if ccs:
                cc = list(sorted(ccs))[0]
                midmap = mod.controller_midi_maps[ctl.name]
                midmap.message_type = MidiMessageType.control_change
                midmap.message_parameter = cc

    def compile_parameters(self):
        self.parameters_manager.parameters = self.kit.parameter_module.p

    def compile_project(self):
        self.clear_midi_mapping()
        self.clear_udc_list()
        self.clear_udc_widgets()
        self.kit.parameter_values_dirty = True
        module = self.kit.project_module
        self.setup_sunvox_slot()
        self.slot.load(module.project)
        self.controllers_manager.root_group = module.c

    def set_compile_actions_enabled(self):
        self.action_compile_parameters.setEnabled(
            not self.kit.parameter_factory_source_clean)
        self.action_compile_project.setEnabled(True)
        self.parameter_compile_button.setEnabled(
            self.action_compile_parameters.isEnabled())
        self.project_compile_button.setEnabled(
            self.action_compile_project.isEnabled())

    def set_controllers_width(self):
        self.scrollarea_4.setMinimumWidth(
            self.scrollarea_4.widget().width())

    def set_parameters_source(self):
        self.kit.parameter_factory_source = self.parameter_editor.text

    def set_parameters_width(self):
        self.scrollarea_2.setMinimumWidth(
            self.scrollarea_2.widget().width())

    def set_project_source(self):
        self.kit.project_factory_source = self.project_editor.text

    def update_udc_widgets(self):
        self.clear_udc_widgets()
        for i, name in enumerate(self.udc_list, 1):
            label = QLabel('{}: {}'.format(i, name), self)
            self.layout_5.addWidget(label)
        self.layout_5.addStretch(1)

    @pyqtSlot()
    def on_action_compile_parameters_triggered(self):
        with OutputCatcher(self.parameter_output):
            # noinspection PyBroadException
            try:
                self.compile_parameters()
            except Exception:
                print(traceback.format_exc())
        self.set_compile_actions_enabled()
        QTimer.singleShot(1, self.set_parameters_width)

    @pyqtSlot()
    def on_action_compile_project_triggered(self):
        with OutputCatcher(self.project_output):
            # noinspection PyBroadException
            try:
                self.compile_project()
                self.auto_map_controllers()
            except Exception:
                print(traceback.format_exc())
            else:
                self.kit.parameter_values_dirty = False
        self.set_compile_actions_enabled()
        QTimer.singleShot(1, self.set_controllers_width)

    @pyqtSlot(str, str)
    def on_controllers_manager_mapping_changed(self, alias, name):
        # first remove existing controller/alias mappings
        for a in list(self.controller_aliases[name]):
            if name in self.alias_controllers[a]:
                self.alias_controllers[a].remove(name)
            if a in self.controller_aliases[name]:
                self.controller_aliases[name].remove(a)
        self.alias_controllers[alias].add(name)
        self.controller_aliases[name].add(alias)

    @pyqtSlot(int, str)
    def on_controllers_manager_value_changed(self, value, name):
        controller = self.kit.project_module.c[name]
        mod = controller.module.index + 1
        ctl = controller.ctl.number
        pvalue = controller.ctl.pattern_value(value)
        self.slot.send_event(0, 0, 0, mod, ctl << 8, pvalue)

    @pyqtSlot(bool, str)
    def on_controllers_manager_udc_changed(self, state, name):
        if state and name not in self.udc_list:
            self.udc_list.append(name)
        elif not state and name in self.udc_list:
            self.udc_list.remove(name)
        self.update_udc_widgets()

    @pyqtSlot(str, 'PyQt_PyObject')
    def on_midi_listener_message_received(self, port_name, message):
        note_on = message.type == 'note_on'
        note_off = message.type == 'note_off'
        cc = message.type == 'control_change'
        if note_on and message.velocity > 0:
            note = message.note - 24 + 1
            self.slot.send_event(0, note, message.velocity, 2, 0, 0)
            self._active_playback_notes += 1
        elif note_off or (note_on and message.velocity == 0):
            self._active_playback_notes -= 1
            self._active_playback_notes = max(self._active_playback_notes, 0)
            if self._active_playback_notes == 0:
                self.slot.send_event(0, NOTECMD.NOTE_OFF, 0, 0, 0, 0)
        elif cc:
            for alias in cc_mappings.cc_aliases[message.control]:
                for name in self.alias_controllers[alias]:
                    # map message.value to controller range
                    if name not in self.kit.project_module.c:
                        continue
                    c = self.kit.project_module.c[name]
                    ctl = c.ctl
                    value_type = ctl.value_type
                    if isinstance(value_type, Range):
                        min_value, max_value = value_type.min, value_type.max
                    elif isinstance(value_type, type) and issubclass(value_type, Enum):
                        min_value, max_value = 0, len(value_type)
                    elif value_type is bool:
                        min_value, max_value = 0, 1
                    range = max_value - min_value
                    factor = range / 127.0
                    value = int(message.value * factor)
                    value += min_value
                    self.controllers_manager.set_ctl_value(name, value)

    @pyqtSlot()
    def on_parameter_editor_debouncer_timeout(self):
        self.set_parameters_source()
        self.set_compile_actions_enabled()

    @pyqtSlot()
    def on_parameter_editor_textChanged(self):
        if self.parameter_editor_debouncer is not None:
            self.parameter_editor_debouncer.stop()
        t = self.parameter_editor_debouncer = QTimer(self)
        t.setSingleShot(True)
        t.timeout.connect(self.on_parameter_editor_debouncer_timeout)
        t.start(DEBOUNCE_MSEC)

    @pyqtSlot()
    def on_parameters_manager_valuesChanged(self):
        self.kit.parameter_values_dirty = True
        self.set_compile_actions_enabled()

    @pyqtSlot()
    def on_project_editor_debouncer_timeout(self):
        self.set_project_source()
        self.set_compile_actions_enabled()

    @pyqtSlot()
    def on_project_editor_textChanged(self):
        if self.project_editor_debouncer is not None:
            self.project_editor_debouncer.stop()
        t = self.project_editor_debouncer = QTimer(self)
        t.setSingleShot(True)
        t.timeout.connect(self.on_project_editor_debouncer_timeout)
        t.start(DEBOUNCE_MSEC)

    def load_json(self, data):
        self.kit.load_json(data)
        self.parameters_manager.clear_widgets()
        self.controllers_manager.clear_widgets()
        self.clear_midi_mapping()
        self.clear_udc_list()
        self.clear_udc_widgets()
        self.parameter_editor.setPlainText(self.kit.parameter_factory_source)
        self.project_editor.setPlainText(self.kit.project_factory_source)


SAMPLE_PARAMETER_FACTORY = """\
from sf.mmck.parameters import *

# Define your parameters below by adding to the
# `p` object.
#
# You can define String or Integer parameters.
#
# Example:
#
#   p.name = String(label='Project Name')
#   p.voices = Integer(5, range=(3, 17), step=2)
#   p.spread = Integer(5, range=(0, 128))

p.name = String(label='Project Name')
"""


SAMPLE_PROJECT_FACTORY = """\
from sf.mmck.project import *
from rv.api import *

# Construct the MetaModule interior by
# attaching modules to the `project` object.
# Consult the `rv` documentation for details.
# http://radiant-voices.rtfd.io/
#
# Expose controllers you'd like to manipulate
# by adding them to the `c` object, using
# `(module, ctl_name)` notation.
#
# Group them together using `Group` objects.
#
# Example:
#
#   gen = project.new_module(
#       m.AnalogGenerator,
#       polyphony_ch=1,
#       sustain=False,
#   )
#   gen >> project.output
#   c.attack = (gen, 'attack')
#   c.release = (gen, 'release')

project.name = p.name or 'My Synth'
"""
