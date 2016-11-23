from PyQt5.QtWidgets import QComboBox


class EnumWidget(QComboBox):

    def __init__(self, parent, value_type, initial_value):
        super().__init__(parent)
        self.index_values = {}
        self.value_indexes = {}
        for index, option in enumerate(value_type):
            self.addItem(option.name, option.value)
            self.index_values[index] = option.value
            self.value_indexes[option.value] = index
        self.setCurrentIndex(self.value_indexes[initial_value.value])
