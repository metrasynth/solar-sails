from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class ParameterWidget(QWidget):

    valueChanged = pyqtSignal('PyQt_PyObject', str)  # value, name

    def __init__(self, parent, name, parameter, value):
        super().__init__(parent)
        self.name = name
        self.parameter = parameter
        self.value = value
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setUp(self)

    def setUp(self, ui):
        self.setup_label()

    def setup_label(self):
        self.label = QLabel(self.name, self)
        self.layout.addWidget(self.label)
