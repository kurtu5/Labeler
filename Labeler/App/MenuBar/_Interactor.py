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

from PySide2.QtWidgets import QAction

class Interactor(MVPBase.BaseInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

    def event_all_register(self):

        self.event_add((self.view.file_menu_quit,'triggered', self.presenter.on_app_exit))

        def on_window_enable(action):
            print("on window enable")
            self.presenter.on_window_enable(action.data())
        self.event_add((self.view.view_menu,('triggered', QAction), on_window_enable))
#        self.event_add((self.view.view_menu,'triggered', on_window_enable))


