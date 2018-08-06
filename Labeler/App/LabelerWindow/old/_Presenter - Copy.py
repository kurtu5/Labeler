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
        self.scale_xloc = 0  # TODO maybe shove these into view
        self.scale_yloc = 0
        self.image_index = None
        self.start()

    def start(self):
        super().start()
        # TODO This stuff should be pulled from model and set to model
        self.shortcuts_labels = {"q": "feat1", "w": "feat2", "e": "feat3", "r": "other"}
        self.labels = {}  # TODO When controller loads image, should set this from csv



## TODO where do these belong?
    def image_load(self):
        self.model.get_image()
        self.view.image_load(self.model.image_file)

    def image_update(self):
        # Update status string
        status_text = f'index: {self.model.image_index} image: {self.model.image_file} scale: {self.scale:.2f}'
        self.model.status_text_update(status_text)

        image_count = len(self.model.get_images())
        self.view.image_listbox.select_clear(0, image_count)
        self.view.image_listbox.see(self.model.image_index)

        self.view.image_listbox.select_set(self.model.image_index)
        self.view.image_update(self.scale, self.scale_xloc, self.scale_yloc)

## deal with labeling shortcuts

    def label(self, key, has_feature = None):
        """ set label on image and update view """
        # Cycle through labels
        if has_feature == None:
            cycle = [-1, 0, 1]
            if key not in self.labels:
                current = 0
            else:
                current = self.labels[key]
            has_feature = cycle[(cycle.index(current)+1)%len(cycle)]
        # Set
        self.labels[key] = has_feature
        self.view.set_label_widget(key, has_feature)


    ### Base Presenter method overrides
    def on_window_enable(self, enable):
        super().on_window_enable(enable)
        if enable == True:
            self.refresh_images()

    def refresh_images(self):
            self.scale = self.default_scale
            self.model.refresh_images()
            self.image_load()
            self.image_update()
            self.view.canvas.focus_set()
            images = self.model.get_images()
            self.interactor.image_list_set(images)

    ### View Interactor event handlers
    def on_scale(self, scale, event):
        if scale == 1:
            self.scale = 1.0
        else:
            self.scale *= scale;
            self.scale_xloc = event.x
            self.scale_yloc = event.y
        self.image_update()

    def on_scroll(self, amount):
        self.view.scroll(amount)

    def on_mouse_wheel(self, event):
        amount = 0
        # Deal with linux and windows events
        if event.num == 5 or event.delta == -120:
            amount += 1
        elif event.num == 4 or event.delta == 120:
            amount -= 1
        self.on_scroll(amount)

    def on_keyevent(self, event):
        D.ebug(f'Labeler keyevent  event={event}  event.state={event.state}')
        if event.keysym == 'space' or event.keysym == 'Down':
            self.on_scroll(2)
        if event.keysym == 'Up':
            self.on_scroll(-2)
        if event.keysym == 'Right':
#            self.scale = self.default_scale
            self.model.next_image()
            self.image_load()
            self.image_update()
        if event.keysym == 'Left':
#            self.scale = self.default_scale
            self.model.prev_image()
            self.image_load()
            self.image_update()
        # Pass to shortcut to check if one was used
        self.on_keyshortcut(event)



    # TODO this is so view specific, move to view/interactot
    def on_keyshortcut(self, event):
        """ Use shortcuts to label features as 0=no 1=yes -1=unknown """
        control = 4
        shift = 1
        alt = 131072
        state = event.state
        key = event.keysym
        key = key.lower()
        has_feature = None
        # toggle if only the key was pressed
        # control = no feature
        # alt = unknown
        # shift= set feature
        D.ebug(f'event.keysym = {event.keysym}' )

        if key in self.shortcuts_labels:
            if state & alt:
                has_feature = -1
            elif state & shift:
                has_feature = 1
            elif state & control:
                has_feature = 0
            else:
                has_feature = None
            self.label(key, has_feature)

    ### Model Observer event handlers