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

class Presenter(MVPBase.PresenterBase):
    def __init__(self, *args, **kwargs):
#         print('menubar P init')
        super().__init__(*args, **kwargs)
        self.start()
        
    def start(self):
        super().start()
    
    def closeapp(self):
        # Just call the gui model as no menu states need to change
        self.model.other_models['gui'].closeapp()
    
    def show_window(self, window_name):
        self.model.other_models['gui'].window_current(window_name)
#         print('call raise in guimodel to raise the class window')