# -*- coding: utf-8 -*-

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import MVPBase

from PySide2.QtWidgets import QMenu, QAction

class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
            super().start()

            # File Menu
            self.file_menu = QMenu("&File")
            self.file_menu_quit = QAction("E&xit", self.file_menu)
            self.file_menu.addAction(self.file_menu_quit)

            # Window Menu
            self.view_menu = QMenu("&View")
            act = QAction("&Labeler", self.view_menu)
            act.setData("labeler")
            self.view_menu.addAction(act)

            act = QAction("&Test", self.view_menu)
            act.setData("test")
            self.view_menu.addAction(act)

            act = QAction("&Options", self.view_menu)
            act.setData("options")
            self.view_menu.addAction(act)

            # Edit Menu
            self.edit_menu = QMenu("&Edit")
            self.edit_menu.addAction("delete")

            # Add them all
            self.parent.window.menuBar().addMenu(self.file_menu)
            self.parent.window.menuBar().addMenu(self.view_menu)
            self.parent.window.menuBar().addMenu(self.edit_menu)

