from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLineEdit
from sf.mmck.parameters import String
from .manager import widget_class_for
from .widget import ParameterWidget


@widget_class_for(String)
class StringParameterWidget(ParameterWidget):

    def setUp(self, ui):
        super().setUp(ui)
        self.lineedit = QLineEdit(self)
        self.lineedit.setText(self.value)
        self.lineedit.textChanged.connect(self.on_lineedit_textChanged)
        self.layout.addWidget(self.lineedit)

    @pyqtSlot(str)
    def on_lineedit_textChanged(self, value):
        self.valueChanged.emit(value, self.name)
