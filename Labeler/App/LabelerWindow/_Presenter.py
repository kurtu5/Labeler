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
from tkCustom._Debug import D
from PIL import ImageTk, Image
 
class Presenter(MVPBase.BasePresenter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_scale = 1.0
        self.scale = self.default_scale
        self.scale_xloc = 0
        self.scale_yloc = 0
        self.image_file = None
        self.image_index = None
        self.start()
        
    def start(self):
        super().start()
        
         # Let guiM know im showable
        self.model.other_models['gui'].window_add('labeler', self.view.get_root())
        self.image_load()
        self.image_show()

    def image_load(self):
        self.image_file = self.model.other_models['images'].current_image
        self.image_index = self.model.other_models['images'].index
        self.view.image_load(self.image_file)
    
    def image_show(self):
        # Update status string
        self.model.other_models['gui'].status_text.set(f'index: {self.image_index}  image: {self.image_file}  scale: {self.scale:.2f}')
        self.view.image_update(self.scale, self.scale_xloc, self.scale_yloc)
        
    def on_scale(self, scale, event):
#         print("scale", self.scale, "eventxy", event.x, event.y)
        if scale == 1:
            self.scale = 1.0
        else:
            self.scale *= scale;
            self.scale_xloc = event.x
            self.scale_yloc = event.y
        self.image_show()
    
    def on_scroll(self, amount):
        self.view.scroll(amount)
        

    def on_mouse_wheel(self, event):
#         print("mouse scroll","scroll",event.delta,"units")
        amount = 0
        # Deal with linux and windows events
        if event.num == 5 or event.delta == -120:
            amount += 1
        elif event.num == 4 or event.delta == 120:
            amount -= 1
#         print("scroll by ", amount)
        self.on_scroll(amount)      
        
    def on_keyevent(self, event):
        D.ebug(f'event={event}')
        if event.keysym == 'space' or event.keysym == 'Down':
            self.on_scroll(2)
        if event.keysym == 'Up':
            self.on_scroll(-2)
        if event.keysym == 'Right':
            self.model.other_models['images'].next() 
            self.image_load()
            self.image_show()
        if event.keysym == 'Left':
            self.model.other_models['images'].prev()
            self.image_load()
            self.image_show()

        
        
