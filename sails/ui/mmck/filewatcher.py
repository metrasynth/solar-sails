import os

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal


class FileWatcher(QObject):

    fileChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.paths = []
        self._current_mtimes = {}
        self._current_sizes = {}
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(100)

    @pyqtSlot()
    def on_timer_timeout(self):
        emit = False
        found_mtimes = []
        found_sizes = []
        for path in self.paths:
            try:
                s = os.stat(path)
            except FileNotFoundError:
                pass
            else:
                if self._current_mtimes.get(path) is None:
                    self._current_mtimes[path] = s.st_mtime
                    self._current_sizes[path] = s.st_size
                if self._current_mtimes[path] != s.st_mtime or self._current_sizes[path] != s.st_size:
                    self._current_mtimes[path] = s.st_mtime
                    self._current_sizes[path] = s.st_size
                    emit = True
        if emit:
            self.fileChanged.emit()
