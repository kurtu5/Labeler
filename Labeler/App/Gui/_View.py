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

# set in super        self.root = root # tk.Tk() 1 col 1 row; holds main

    def debugFrame(self, parent, text, on=True):
        if self.debug == True:
            return self.tk.LabelFrame(parent, text=text)
        elif self.debug == False:
            return self.tk.Frame(parent)

    def start(self, *a, **kw):
        self.root.grid_columnconfigure(0, weight=1) # have main fill on resize
        self.root.grid_rowconfigure(0, weight=1)
#         self.root.resizable(0,0)
        self.root.grid_propagate(0)
        self.debug=False
        #main
        self.main=self.debugFrame(self.root, text='main')  # has 1 col and 2 rows; w and s
        self.main.grid_columnconfigure(0, weight=1)  # widen both w and s
        self.main.grid_rowconfigure(0, weight=1)  # heighten only w
#         self.main.grid_rowconfigure(1, weight=0)
        self.main.grid(column=0, row=0, sticky='nsew') # Fill root parent


        #window
        self.window = self.debugFrame(self.main, text='window') # has 1col 1 row; new windows go here
        self.window.grid_columnconfigure(0, weight=1) # window will widen and heighten on resize
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid(column=0, row=0, sticky='nsew') # fill cell in main

        # Debugger bar
        debug = self.tkc.D(self.main, 8)
        debug.frame.grid(column=0, row=1, sticky='we')

        #status bar
        self.statusbar = self.debugFrame(self.main, text='statusbar') # has 1 row 2 col; has status text and grip
        self.statusbar.grid_columnconfigure(0, weight=1) # status text will widen on resize
        # self.statusbar.grid_columnconfigure(1, weight=1) # sizegrip will widen on resize
        self.statusbar.grid(column=0, row=2, sticky='we') # widen cell in main


        #statustext and sizegripper
        self.statusframe = self.debugFrame(self.statusbar, text='statustext') # 1 row 1 col; has actual text
        self.statusframe.grid_columnconfigure(0, weight=1)  # actual text will widen on resize
        self.statusframe.grid(column=0, row=0, sticky='we')

        self.statustext = self.tk.Label(self.statusframe, text="some status line text")
        self.statustext.pack()

        self.grip = self.tkc.AutoSizegrip(self.statusbar, self.root)
        self.grip.grid(column=1, row=0, sticky='nsew')

        self.root.geometry('1500x800+50+50')
#         self.root.wm_attributes("-topmost", 1)  # Always on top

        self.root.lift()
        self.root.focus_force()
#         self.current_window_class = None


    # Methods for presenter to call
    def window_show(self, window_root):
        window_root.tkraise()

    def status_text_set(self, text):
        self.statustext.config(text=text)

    def app_exit(self):
        self.root.destroy()