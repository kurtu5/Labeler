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

class Presenter(MVPBase.BasePresenter):
    def __init__(self, *args, **kwargs):
#         print('menubar P init')
        super().__init__(*args, **kwargs)
        self.start()

    def start(self):  
        super().start()

    def on_app_exit(self):
        self.model.app_exit()

    def on_window_show(self, window_name):
        self.model.window_show(window_name)
