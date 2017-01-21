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

from .controllers.manager import ControllersManager
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

    def clear_udc_list(self):
        self.udc_list = []

    def clear_udc_widgets(self):
        while self.layout_5.count() > 0:
            child = self.layout_5.takeAt(0)
            w = child.widget()
            if w:
                w.close()
                w.deleteLater()

    def update_udc_widgets(self):
        self.clear_udc_widgets()
        for i, name in enumerate(self.udc_list, 1):
            label = QLabel('{}: {}'.format(i, name), self)
            self.layout_5.addWidget(label)
        self.layout_5.addStretch(1)

