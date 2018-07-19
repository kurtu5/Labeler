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
#       Use this if this is a applicaion window
#        self.window_enable = False


    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
#        Use this if this is a applicaion window
#        self.window_enable = self.observer.observe_as('window_enable', False)

