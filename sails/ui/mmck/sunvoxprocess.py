from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import qApp

from sunvox.api import Process, Slot


class SunvoxProcess(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sunvox = Process()
        self.sunvox.init(None, 44100, 2, 0)
        qApp.aboutToQuit.connect(self.shutdown)

    @property
    def slot(self):
        if not hasattr(self, '_slot'):
            self._slot = Slot(process=self.sunvox)
            self._slot.volume(256)
        return self._slot

    @slot.deleter
    def slot(self):
        if hasattr(self, '_slot'):
            self._slot.close()
            del self._slot

    def shutdown(self):
        try:
            del self.slot
            self.sunvox.deinit()
        finally:
            self.sunvox.kill()
