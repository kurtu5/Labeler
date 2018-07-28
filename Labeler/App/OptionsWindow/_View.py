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

    def start(self):
        tk = self.tk
        self.main = tk.Frame(self.root)
        main = self.main
        main.grid(column=0, row=0, sticky='nsew')
        main.grid_columnconfigure(0, weight=0)
        main.grid_columnconfigure(1, weight=0)
        tk.Label(main, text="Options go here").grid(row=0)
        el1 = tk.Label(main, text="Path to image files: ")
        el1.grid(row=1)
        el2 = tk.Label(main, text="Last Name")
        el2.grid(row=2)


        self.e1Button = tk.Button(main, text="Change", command=lambda: print('pressed'))
        self.e1Button.grid(row=1, column=3)
        self.e1 = tk.Entry(main)
        self.e2 = tk.Entry(main)
        
        self.e1.grid(row=1, column=2)
        self.e2.grid(row=2, column=2)
