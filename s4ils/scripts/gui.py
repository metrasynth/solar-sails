import asyncio
import sys

import begin
from PyQt5.QtWidgets import QApplication, QMainWindow
from quamash import QEventLoop

from s4ils.ui.mainmenubar import MainMenuBar


@begin.start
def main():
    """Start the S4ils GUI."""
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    main_window = QMainWindow()
    main_window.setMenuBar(MainMenuBar())
    main_window.show()
    loop.run_forever()
