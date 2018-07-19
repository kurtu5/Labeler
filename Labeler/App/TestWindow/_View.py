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

    def start(self):
        self.main = self.tk.LabelFrame(self.root, text="test main")
        self.main.grid(column=0, row=0, sticky='nsew')
        self.main.grid_columnconfigure(0, weight=1)
        self.tk.Label(self.main, text="bt 1 disables button 2").grid()
        self.lf = self.tk.LabelFrame(self.main, text="bound things")
        self.lf.grid(sticky='ew')
        self.lf.grid_columnconfigure(0, weight=1)
        self.lb = self.tk.Label(self.lf, text="1 may do 2 things,  2 disables second, 3 enables it")
        self.lb.grid(sticky='ew')