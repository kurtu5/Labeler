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

class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Setup basic window manager """
     
    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        
