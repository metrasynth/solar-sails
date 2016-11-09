import logging
import os

from PyQt5.QtWidgets import QFileDialog


class Opener(object):

    file_ext = None
    file_type_label = None
    main_window_class = None

    _open_file_windows = {
        # filename: main_window
    }

    _opener_classes = {
        # file-extension: opener-class
    }

    def __init__(self, parent):
        self.parent = parent

    @property
    def caption(self):
        return 'Open {} file'.format(self.file_type_label)

    @property
    def filter(self):
        return '{} Files (*{})'.format(self.file_type_label, self.file_ext)

    @classmethod
    def open_file(cls, filename):
        _, ext = os.path.splitext(filename)
        opener_class = cls._opener_classes.get(ext)
        if opener_class:
            return opener_class.new_or_existing_window(filename)
        else:
            logging.warning('%r files not supported', ext)

    @classmethod
    def register_opener(cls, subclass):
        cls._opener_classes[subclass.file_ext] = subclass
        return subclass

    @classmethod
    def remove_file_window(cls, filename):
        if filename in cls._open_file_windows:
            del cls._open_file_windows[filename]

    @classmethod
    def new_or_existing_window(cls, filename):
        if filename not in cls._open_file_windows:
            window = cls.main_window_class(filename=filename)
            cls._open_file_windows[filename] = window
            window.setWindowFilePath(filename)
            logging.debug('File %r opened', filename)
        else:
            logging.debug('File %r already open', filename)
            window = cls._open_file_windows[filename]
        return window

    def requested_filename(self, directory='.'):
        return QFileDialog.getOpenFileName(
            parent=self.parent,
            caption=self.caption,
            directory=directory,
            filter=self.filter,
        )

    def exec_(self, filename=None):
        if filename is None:
            filename, _ = self.requested_filename()
        if filename:
            _, ext = os.path.splitext(filename)
            opener_class = self._opener_classes[ext]
            return opener_class.new_or_existing_window(filename)
        else:
            return None
