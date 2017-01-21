import os

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal


class FileWatcher(QObject):

    fileChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = None
        self._current_mtime = None
        self._current_size = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(100)

    @pyqtSlot()
    def on_timer_timeout(self):
        if self.path is not None:
            try:
                s = os.stat(self.path)
            except FileNotFoundError:
                return
            else:
                if self._current_mtime is None:
                    self._current_mtime = s.st_mtime
                    self._current_size = s.st_size
                if self._current_mtime != s.st_mtime or self._current_size != s.st_size:
                    self._current_mtime = s.st_mtime
                    self._current_size = s.st_size
                    self.fileChanged.emit()
        else:
            self._current_mtime = None
            self._current_size = None
