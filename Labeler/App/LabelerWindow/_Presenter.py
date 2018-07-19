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
        # This stuff should be pulled from model and set to model
        self.shortcuts_labels = {"q": "feat1", "w": "feat2", "e": "feat3", "r": "other"}
        self.labels = {}  # When controller loads image, should set this from csv

         # Let guiM know im showable
        self.model.others['gui'].window_add('labeler', self.view.get_root())
        self.image_load()
        self.image_show()

    def image_load(self):
        self.image_file = self.model.others['images'].current_image
        self.image_index = self.model.others['images'].index
        self.view.image_load(self.image_file)

    def image_show(self):
        # Update status string
        self.model.others['gui'].status_text.set(f'index: {self.image_index}  image: {self.image_file}  scale: {self.scale:.2f}')
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
            self.model.others['images'].next()
            self.image_load()
            self.image_show()
        if event.keysym == 'Left':
            self.model.others['images'].prev()
            self.image_load()
            self.image_show()
        # Pass to shortcut to check if one was used
        self.on_keyshortcut(event)

    def on_keyshortcut(self, event):
        """ Use shortcuts to label features as 0=no 1=yes -1=unknown """
        key = event.char
        has_feature = None
        if key in self.shortcuts_labels:
#           # Label it 1 if it doesn't exist or was 0
            if key not in self.labels or self.labels[key] == 0 or self.labels[key] == -1:
                has_feature = 1
            # Label it 0 otherwise
            elif self.labels[key] == 1:
                has_feature = 0
            # If the Shift modifier set as unknown
        if key.isupper() and key.lower() in self.shortcuts_labels:
            has_feature = -1
            key = key.lower()
        if has_feature != None:
            self.labels[key] = has_feature
            self.view.set_label_widget(key, has_feature)
            # set labels in model



