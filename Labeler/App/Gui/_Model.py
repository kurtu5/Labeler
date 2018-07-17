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

class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_map = {}  # name => root
        self.window_current = None
        self.status_text = None
    
    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        self.app_exit = self.observer.observe_as('app_exit', False)
        self.window_current = self.observer.observe_as('window_current', False)
        self.status_text = self.observer.observe_as('status_text')

    def window_add(self, name, root):
        self.window_map[name] = root
        
    def window_show(self, name):
        self.window_current.set(name)

    def app_exit(self):
        # TODO add sanity checking to see if things need to be saved
        self.app_exit.set(True)