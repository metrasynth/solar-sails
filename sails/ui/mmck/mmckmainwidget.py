import os

from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUiType
from qutepart import Qutepart

UIC_NAME = 'mmckmainwidget.ui'
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)


Ui_MmckMainWidget, MmckMainWidgetBase = loadUiType(UIC_PATH)


class MmckMainWidget(MmckMainWidgetBase, Ui_MmckMainWidget):

    def __init__(self, parent=None):
        super(MmckMainWidget, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, ui):
        super(MmckMainWidget, self).setupUi(ui)
        self.setup_parameter_editor()
        self.setup_project_editor()
        self.stub2 = QFrame(self)
        self.stub4 = QFrame(self)
        self.stub5 = QFrame(self)
        self.layout_2.addWidget(self.stub2)
        self.layout_4.addWidget(self.stub4)
        self.layout_5.addWidget(self.stub5)

    def setup_parameter_editor(self):
        editor = self.parameter_editor = Qutepart(self)
        editor.setMinimumWidth(300)
        p = editor.sizePolicy()
        p.setVerticalPolicy(p.Expanding)
        editor.detectSyntax(language='Python')
        editor.setPlainText(SAMPLE_PARAMETER_FACTORY)
        self.layout_1.addWidget(editor)

    def setup_project_editor(self):
        editor = self.project_editor = Qutepart(self)
        editor.setMinimumWidth(300)
        p = editor.sizePolicy()
        p.setVerticalPolicy(p.Expanding)
        editor.detectSyntax(language='Python')
        editor.setPlainText(SAMPLE_PROJECT_FACTORY)
        self.layout_3.addWidget(editor)


SAMPLE_PARAMETER_FACTORY = """\
from sf.mmck.parameters import *

p.name = String(label='Project Name')
p.voices = Integer(5, min=3, max=17, step=2)
p.spread = Integer(5, min=0, max=128)
"""


SAMPLE_PROJECT_FACTORY = """\
from sf.mmck.parameters import *
from rv.api import *

project = Project()
project.name = p.name

start = -(p.voices - 1) / 2
end = start + p.voices
saws = [
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
    for x in range(start, end + 1)
]
multi = project.new_module(
    m.MultiSynth,
    random_phase=32768,
)
multi >> saws >> project.output

project.layout()
"""
