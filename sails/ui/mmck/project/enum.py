from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QComboBox


class EnumWidget(QComboBox):

    value_changed = pyqtSignal(int)

    def __init__(self, parent, value_type, initial_value):
        super().__init__(parent)
        self.index_values = {}
        self.value_indexes = {}
        for index, option in enumerate(value_type):
            self.addItem(option.name, option.value)
            self.index_values[index] = option.value
            self.value_indexes[option.value] = index
        self.setCurrentIndex(self.value_indexes[initial_value.value])
        self.currentIndexChanged.connect(self.on_currentIndexChanged)

    @pyqtSlot(int)
    def on_currentIndexChanged(self, index):
        value = self.index_values[index]
        self.value_changed.emit(value)
