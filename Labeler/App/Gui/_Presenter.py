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

class Presenter(MVPBase.BasePresenter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Deals with setting/unsetting binds and window management """
#        self.window_current = None
#        self.model.statustext = None
        self.start()

    def start(self):
        super().start()
#        self.view.window_show(self.model.window_map['labeler'])

    ### View Interactor event handlers
    def on_keypress(self, key):
        if ( key == 'Escape'):
            # Let the model decide what to do on app_exit
            self.model.app_exit.set(True)
    
    ### Model Observer event handlers
    def on_app_exit(self):
        self.view.app_exit()
        
    # As directed by model when window_current changes
    def on_window_show(self, window_name):
        print("show win", self.model.window_map)
        self.view.window_show(self.model.window_map[window_name])
        
    def on_status_text(self, text):
        self.view.status_text_set(text)
