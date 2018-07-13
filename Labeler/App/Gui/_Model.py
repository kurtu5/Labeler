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

class Model(MVPBase.ModelBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.windows_showable = {}
        self.windowname_current = None
    
    def window_showable_add(self, windowname, widget):
        self.windows_showable[windowname] = widget
        
    def window_current(self, windowname):
#         print(f'windowname is now {windowname}')
        self.presenter.window_current.set(self.windows_showable[windowname])

    def closeapp(self):
        self.presenter.closeapp()