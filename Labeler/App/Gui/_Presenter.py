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
        self.start()

    def start(self):
        super().start()
        self.interactor.event_all_activate()
        self.observer.event_all_activate()
        
    ### Base Presenter method overrides

    ### View Interactor event handlers
    def on_keypress(self, event):
        from tkCustom._Debug import D
        D.ebug(f'GUI keypress event={event}')
        key = event.keysym
        if ( key == 'Escape'):
            # Let the model decide what to do on app_exit
            self.model.app_exit.set(True)
            
        if ( key == '1'):
            self.model.window_model_activate('test')
        if ( key == '2'):
            self.model.window_model_activate('labeler')
        if ( key == '3'):
            self.model.window_model_activate('options')
        # Control+o
        if event.state & 4 and event.keysym=='o':
            self.app_open()

    ### Model Observer event handlers
    def on_app_exit(self):
        self.view.app_exit()

    def on_status_text(self, text):
        self.view.status_text_set(text)
        
    def app_open(self):
        file = self.view.app_open()
        self.view.status_text_set(f'app open called and got {file}')

