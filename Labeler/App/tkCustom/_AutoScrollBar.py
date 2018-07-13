# -*- coding: utf-8 -*-
import tkinter as tk

class AutoScrollbar(tk.Scrollbar):
#     def __init__(self):
#         tk.Scrollbar.__init__(self)
#         # a scrollbar that hides itself if it's not needed.  only
#         # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.grid_remove()
        else:
            self.grid()
            tk.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise tk.TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise tk.TclError("cannot use place with this widget")