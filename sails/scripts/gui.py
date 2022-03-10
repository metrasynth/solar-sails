import asyncio
import sys

import begin
from PyQt6.QtWidgets import QMainWindow
from quamash import QEventLoop
from sails import midi
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
    midi.load()
    midi.listener.update_ports()
    virtual = sys.platform != 'win32'
    midi.listener.start_port_listener('Metrasynth Solar Sails', virtual=virtual)
    app.aboutToQuit.connect(midi.listener.stop)
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
            window.setFocus()
    loop.run_forever()
