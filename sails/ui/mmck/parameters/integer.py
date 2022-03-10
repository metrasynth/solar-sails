from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QSpinBox
from sf.mmck.parameters import Integer
from .manager import widget_class_for
from .widget import ParameterWidget


@widget_class_for(Integer)
class IntegerParameterWidget(ParameterWidget):

    def setUp(self, ui):
        super().setUp(ui)
        self.spinbox = QSpinBox(self)
        self.spinbox.setSingleStep(self.parameter.step)
        if self.parameter.range is not None:
            min_, max_ = self.parameter.range
            self.spinbox.setMinimum(min_)
            self.spinbox.setMaximum(max_)
        self.spinbox.setValue(self.value)
        self.spinbox.valueChanged.connect(self.on_spinbox_valueChanged)
        self.layout.addWidget(self.spinbox)

    @pyqtSlot(int)
    def on_spinbox_valueChanged(self, value):
        self.valueChanged.emit(value, self.name)
