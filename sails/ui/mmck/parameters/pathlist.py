from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QPlainTextEdit
from sf.mmck.parameters import PathList
from .manager import widget_class_for
from .widget import ParameterWidget


@widget_class_for(PathList)
class PathListParameterWidget(ParameterWidget):

    def setUp(self, ui):
        super().setUp(ui)
        self.textedit = QPlainTextEdit(self)
        self.textedit.setPlainText('\n'.join(self.value))
        self.textedit.textChanged.connect(self.on_textedit_textChanged)
        self.textedit.setTabChangesFocus(True)
        self.layout.addWidget(self.textedit)

    @pyqtSlot()
    def on_textedit_textChanged(self):
        value = self.textedit.toPlainText()
        value = [line.strip() for line in value.splitlines() if line.strip()]
        self.valueChanged.emit(value, self.name)
