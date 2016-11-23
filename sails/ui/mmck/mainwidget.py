import os
import traceback

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUiType
from qutepart import Qutepart
from sf.mmck.kit import Kit
from sf.mmck.project import Group
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
        self.kit = Kit()
        self.setupUi(self)

    def setupUi(self, ui):
        super(MmckMainWidget, self).setupUi(ui)
        self.setup_parameter_editor()
        self.setup_parameters()
        self.setup_project_editor()
        self.setup_controllers()
        self.stub4 = QFrame(self)
        self.stub5 = QFrame(self)
        self.layout_4.addWidget(self.stub4)
        self.layout_5.addWidget(self.stub5)
        # noinspection PyCallByClass
        QTimer.singleShot(0, self.parameter_editor.setFocus)

    def setup_controllers(self):
        self.controllers_manager = ControllersManager(
            parent=self.scrollarea_4,
            layout=self.layout_4,
            root_group=EMPTY_GROUP,
        )

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
        self.parameter_exception_browser.hide()

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
        self.project_exception_browser.hide()

    def compile_parameters(self):
        self.parameters_manager.parameters = self.kit.parameter_module.p

    def compile_project(self):
        self.controllers_manager.root_group = self.kit.project_module.c

    def set_compile_buttons_enabled(self):
        self.parameter_compile_button.setEnabled(
            not self.kit.parameter_factory_source_clean)
        self.project_compile_button.setEnabled(
            not self.kit.project_factory_source_clean)

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

    @pyqtSlot()
    def on_action_compile_parameters_triggered(self):
        b = self.parameter_exception_browser
        # noinspection PyBroadException
        try:
            self.compile_parameters()
        except Exception:
            b.setPlainText(traceback.format_exc())
            b.show()
        else:
            b.hide()
        self.set_compile_buttons_enabled()
        QTimer.singleShot(1, self.set_parameters_width)

    @pyqtSlot()
    def on_action_compile_project_triggered(self):
        b = self.project_exception_browser
        # noinspection PyBroadException
        try:
            self.compile_project()
        except Exception:
            b.setPlainText(traceback.format_exc())
            b.show()
        else:
            b.hide()
            self.kit.parameter_values_dirty = False
        self.set_compile_buttons_enabled()
        QTimer.singleShot(1, self.set_controllers_width)

    @pyqtSlot()
    def on_parameter_editor_debouncer_timeout(self):
        self.set_parameters_source()
        self.set_compile_buttons_enabled()

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
        self.set_compile_buttons_enabled()

    @pyqtSlot()
    def on_project_editor_debouncer_timeout(self):
        self.set_project_source()
        self.set_compile_buttons_enabled()

    @pyqtSlot()
    def on_project_editor_textChanged(self):
        if self.project_editor_debouncer is not None:
            self.project_editor_debouncer.stop()
        t = self.project_editor_debouncer = QTimer(self)
        t.setSingleShot(True)
        t.timeout.connect(self.on_project_editor_debouncer_timeout)
        t.start(DEBOUNCE_MSEC)


SAMPLE_PARAMETER_FACTORY = """\
from sf.mmck.parameters import *

p.name = String(label='Project Name')
p.voices = Integer(5, range=(3, 17), step=2)
p.spread = Integer(5, range=(0, 128))
"""


SAMPLE_PROJECT_FACTORY = """\
from sf.mmck.project import *
from rv.api import *

project.name = p.name

start = -(p.voices - 1) // 2
end = start + p.voices
generators = [
    project.new_module(
        m.AnalogGenerator,
        volume=256,
        attack=150,
        release=242,
        polyphony_ch=1,
        sustain=False,
        waveform=m.AnalogGenerator.Waveform.saw,
        finetune=x * p.spread,
    )
    for x in range(start, end)
]
multi = project.new_module(
    m.MultiSynth,
    random_phase=32768,
)
multi >> generators >> project.output

project.layout()

c.random_phase = (multi, 'random_phase')

c.waveforms = Group()
for i, module in enumerate(generators, 1):
    c.waveforms['generator_{}'.format(i)] = (module, 'waveform')
"""
