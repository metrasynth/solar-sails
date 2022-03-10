import sys

from PyQt6.QtWidgets import QPlainTextEdit


class OutputCatcher(object):

    def __init__(self, editor, keep_original=False, clear=True):
        """
        :type editor: QPlainTextEdit
        """
        self.editor = editor
        self.keep_original = keep_original
        self.clear = clear

    @property
    def more(self):
        return OutputCatcher(self.editor, self.keep_original, False)

    def __enter__(self):
        if self.clear:
            self.editor.clear()
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        sys.stdout = OutputWriter(
            self.editor, sys.stdout if self.keep_original else None)
        sys.stderr = OutputWriter(
            self.editor, sys.stderr if self.keep_original else None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr


class OutputWriter(object):

    def __init__(self, editor, file):
        self.editor = editor
        self.file = file

    def flush(self):
        return self.file.flush() if self.file else None

    def write(self, s):
        self.file.write(s) if self.file else None
        self.editor.insertPlainText(s)
        self.editor.ensureCursorVisible()
