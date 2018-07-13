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
import tkinter as tk
import tkCustom as tkc

class View(MVPBase.ViewBase):
    def __init__(self, *args, **kwargs):
#         print('menubarV init')
        super().__init__(*args, **kwargs)
        self.menu = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        
        self.viewmenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='View', menu=self.viewmenu)
        
        
    def start(self):
#             print('============menu started')
            super().start()
            self.root.config(menu=self.menu)
            self.filemenu.add_command(label='Exit', command=self.presenter.closeapp)
            self.viewmenu.add_command(label='Test', command=lambda: self.presenter.show_window('test'))
            self.viewmenu.add_command(label='Labeler', command=lambda: self.presenter.show_window('labeler'))
            self.viewmenu.add_command(label='Generic', command=lambda: self.presenter.show_window('generic'))
