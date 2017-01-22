from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QLabel


class UdcManager(QObject):

    def __init__(self, parent, layout, assignments):
        super().__init__(parent)
        self.layout = layout
        self.assignments = assignments

    @property
    def assignments(self):
        return getattr(self, '_assignments', None)

    @assignments.setter
    def assignments(self, value):
        self._assignments = value
        self.clear()
        for pos, names in enumerate(value, 1):
            num_label = QLabel('{}.'.format(pos), self.parent())
            names_label = QLabel('\n'.join(sorted(names)) if names else '(empty)', self.parent())
            self.layout.addRow(num_label, names_label)

    def clear(self):
        while self.layout.count() > 0:
            child = self.layout.takeAt(0)
            w = child.widget()
            if w:
                w.close()
                w.deleteLater()
