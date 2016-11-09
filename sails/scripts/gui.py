import asyncio
import sys

import begin
from PyQt5.QtWidgets import QMainWindow
from quamash import QEventLoop
from sails.ui.app import App
from sails.ui.mainmenubar import MainMenuBar
from sails.ui.openers import Opener
from sails.ui.welcomewidget import WelcomeWidget

import sails.ui.sun  # NOQA isort:skip


@begin.start
@begin.logging
def main(*filenames: 'Files to open immediately'):
    """Start the Solar Sails GUI."""
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
