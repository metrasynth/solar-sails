from collections import OrderedDict

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPlainTextEdit
from sf.mmck.parameters import KeyValuePairs
from .manager import widget_class_for
from .widget import ParameterWidget


@widget_class_for(KeyValuePairs)
class KeyValuePairsParameterWidget(ParameterWidget):

    def setUp(self, ui):
        super().setUp(ui)
        self.textedit = QPlainTextEdit(self)
        items = self.value.items() if hasattr(self.value, 'items') else self.value
        self.textedit.setPlainText('\n'.join('='.join(item) for item in items))
        self.textedit.textChanged.connect(self.on_textedit_textChanged)
        self.textedit.setTabChangesFocus(True)
        self.layout.addWidget(self.textedit)

    @pyqtSlot()
    def on_textedit_textChanged(self):
        text = self.textedit.toPlainText()
        pairs = [line.strip().split('=') for line in text.splitlines() if line.strip()]
        value = [(items[0].strip(), items[1].strip()) for items in pairs if len(items) == 2]
        self.valueChanged.emit(OrderedDict(value), self.name)
