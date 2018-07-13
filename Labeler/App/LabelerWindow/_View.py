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
from tkinter.font import Font

class View(MVPBase.ViewBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.debug = False

#         self.controller = controller 
        self.label_widgets = {}
        
        self.font = Font(size=24)
        self.default_scale = 0.2
        self.scale = 1.0;   # Initial Image scale
        self.scale_xloc = 0
        self.scale_yloc = 0

        self.main = self.debugFrame(self.root, text="labler main")
        self.main.grid(column=0, row=0, sticky='nsew')
        
#         self.main.grid(column=0, row=1, sticky='nsew')  # 1 col, 2 rows; top bottom
        self.main.grid_columnconfigure(0, weight=1)  # widen top and bottom on resize
        self.main.grid_rowconfigure(1, weight=1)     # heighten bottom on resize
        
#         self.canvas = tk.Canvas()
        # Top frame
        self.top_frame = self.tk.Frame(self.main)
        self.top_frame.grid(column=0, row=0, sticky='ew')  # fill space
        self.top_frame.grid_columnconfigure(0, weight=1) # allow child to widen

        # Bottom
        self.bottom_frame = self.tk.Frame(self.main)
        self.bottom_frame.grid(column=0, row=1, sticky='nsew')
        self.bottom_frame.grid_columnconfigure(0, weight=1) # allow child to fill xy
        self.bottom_frame.grid_rowconfigure(0, weight=1)

#         parent.grid_propagate=(0)

        self.tk.Label(self.top_frame, text='example topframe content').grid(sticky='ew')
#         tk.Label(self.bottom_frame, text='example').grid(sticky='nsew')

        self.canvas_frame = self.debugFrame(self.bottom_frame, text='image')
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid()

        self.xscrollbar = self.tkc.AutoScrollbar(self.canvas_frame, orient='horizontal')
        self.xscrollbar.grid(column=0, row=1, sticky='ew')
#         self.xscrollbar.grid_remove()

        self.yscrollbar = self.tkc.AutoScrollbar(self.canvas_frame, orient='vertical')
        self.yscrollbar.grid(column=1, row=0, sticky='ns')


        self.canvas = self.tk.Canvas(self.canvas_frame,
                        xscrollcommand=self.xscrollbar.set,
                        yscrollcommand=self.yscrollbar.set)
        
        # Binds done in presenter below
        
        self.canvas.grid(row=0, column=0, sticky='nsew')
   
        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)

#         self.create_label_widgets()   # let the models
#         controller.mcs[LabelerMC].update_label_widgets()
    def debugFrame(self, parent, text, on=True):
        if self.debug == True:
            return self.tk.LabelFrame(parent, text=text)
        elif self.debug == False:
            return self.tk.Frame(parent)