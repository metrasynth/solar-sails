import sys

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit


class OutputCatcher(object):

    def __init__(self, editor):
        """
        :type editor: QPlainTextEdit
        """
        self.editor = editor

    def __enter__(self):
        self.editor.clear()
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        sys.stdout = OutputWriter(self.editor, sys.stdout)
        sys.stderr = OutputWriter(self.editor, sys.stderr)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr


class OutputWriter(object):

    def __init__(self, editor, file):
        self.editor = editor
        self.file = file

    def flush(self):
        self.file.flush()

    def write(self, s):
        self.editor.insertPlainText(s)
        self.file.write(s)
