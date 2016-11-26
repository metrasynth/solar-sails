from PyQt5.QtWidgets import QAction, QMenu
from sails.ui.mainmenubar import MainMenuBar


class MmckMainMenuBar(MainMenuBar):

    def create_menus(self):
        super().create_menus()
        self.code_menu = self.addMenu('&Code')
        self.insertMenu(self.tools_menu.menuAction(), self.code_menu)
