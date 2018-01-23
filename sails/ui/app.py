import os, sys

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication


class App(QApplication):

    _singleton = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = QApplication.__new__(cls, *args, **kwargs)
        return cls._singleton

    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.setOrganizationName('Metrasynth')
        self.setOrganizationDomain('metrasynth.warmcommunity.space')
        self.setApplicationName('Solar Sails')
        App.settings = QSettings()
        if sys.platform == 'darwin':
            # Ensure access to GraphViz installed in /usr/local/bin
            os.environ['PATH'] = f"{os.environ['PATH']}:/usr/local/bin"
