import asyncio
import sys

import begin
from PyQt5.QtWidgets import QApplication, QMainWindow
from quamash import QEventLoop

from s4ils.ui.app import App
from s4ils.ui.mainmenubar import MainMenuBar
from s4ils.ui.welcomewidget import WelcomeWidget
from s4ils.ui.openers.opener import Opener
import s4ils.ui.sun


@begin.start
@begin.logging
def main(*filenames: 'Files to open immediately'):
    """Start the S4ils GUI."""
    app = App(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    main_window = QMainWindow()
    main_window.setMenuBar(MainMenuBar())
    welcome_widget = WelcomeWidget(main_window)
    main_window.setCentralWidget(welcome_widget)
    main_window.show()
    for filename in filenames:
        window = Opener.open_file(filename)
        if window:
            window.show()
            window.setFocus(True)
    loop.run_forever()
