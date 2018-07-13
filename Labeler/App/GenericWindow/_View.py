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

class View(MVPBase.ViewBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Setup basic window manager """
        self.main = self.tk.LabelFrame(self.root, text="test main")
        self.main.grid(column=0, row=0, sticky='nsew')
        self.main.grid_columnconfigure(0, weight=1)