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

class Presenter(MVPBase.BasePresenter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Deals with setting/unsetting binds and window management """
        self.start()

    def start(self):
        super().start()
        
    ### Base Presenter method overrides
    def on_window_enable(self, enable):
        super().on_window_enable(enable)
        if enable == True:
#            self.view.e1.config(width=len(self.model.path_to_image_files))
            self.view.e1.delete(0, 'end')
            self.view.e2.delete(0, 'end')
            self.view.e1.config(width=0)
            self.view.e1.insert(10, self.model.path_to_image_files)
            self.view.e2.insert(0, "xxxxxxxxxxx")
            self.view.e2.insert(5, "yyy")
            

    ### View Interactor event handlers
    def change_dir(self, text):
        self.model.path_to_image_files = text

    ### Model Observer event handlers
