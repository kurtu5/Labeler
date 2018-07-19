# -*- coding: utf-8 -*-
#import tkinter as tk
from tkinter import ttk

class AutoSizegrip(ttk.Sizegrip):
    def __init__(self, parent, root, *args, **kwargs):
        ttk.Sizegrip.__init__(self, parent, *args, **kwargs)
        # a sizegrip that hides itself if it's not needed.  only
        # works if you use the grid geometry manager.
        self.root = root
        self.root.bind('<Configure>', self.track)
        
    def track(self, event):
        if self.root.state() == 'zoomed':
            self.grid_remove()
        else:
            self.grid()
            
    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")