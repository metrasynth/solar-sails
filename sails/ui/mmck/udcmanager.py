from PyQt5.QtCore import QObject


class UdcManager(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
