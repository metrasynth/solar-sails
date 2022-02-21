import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.uic import loadUiType


UIC_NAME = "range.ui"
UIC_PATH = os.path.join(os.path.dirname(__file__), UIC_NAME)

Ui_RangeWidget, RangeWidgetBase = loadUiType(UIC_PATH)


class RangeWidget(RangeWidgetBase, Ui_RangeWidget):

    value_changed = pyqtSignal(int)

    def __init__(self, parent, value_type, initial_value):
        self.value_type = value_type
        self.initial_value = initial_value
        self.current_value = initial_value
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, ui):
        super().setupUi(ui)
        min_value = self.value_type.min
        max_value = self.value_type.max
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.spinbox.setMinimum(min_value)
        self.spinbox.setMaximum(max_value)
        self.slider.setValue(self.initial_value)
        self.min_label.setText(str(min_value))
        self.max_label.setText(str(max_value))

    @pyqtSlot(int)
    def on_spinbox_valueChanged(self, value):
        self._set_current_value(value)

    def set_ctl_value(self, value, is_relative):
        if is_relative:
            value += self.current_value
            value = max(min(value, self.value_type.max), self.value_type.min)  # clamp
        self.spinbox.setValue(value)
        self.slider.setValue(value)
        self._set_current_value(value)

    def _set_current_value(self, value):
        self.current_value = value
        self.value_changed.emit(value)
