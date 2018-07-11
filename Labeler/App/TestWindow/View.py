# -*- coding: utf-8 -*-
import MVPBase

class View(MVPBase.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Setup basic window manager """
        self.main = tk.LabelFrame(self.root, text="test main")
        self.main.grid(column=0, row=0, sticky='nsew')
        self.main.grid_columnconfigure(0, weight=1)
        tk.Label(self.main, text="bt 1 disables button 2").grid()
        self.lf = tk.LabelFrame(self.main, text="bound things")
        self.lf.grid(sticky='ew')
        self.lf.grid_columnconfigure(0, weight=1)
        self.lb = tk.Label(self.lf, text="1 may do 2 things,  2 disables second, 3 enables it")
        self.lb.grid(sticky='ew')