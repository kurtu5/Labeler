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

class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_model_map = {}  # model.name => model
        self.window_model_current = None
        self.status_text = None

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        self.app_exit = self.observer.event_gen('app_exit', False)
        self.window_model_current = self.observer.event_gen('window_model_current')
        self.status_text = self.observer.event_gen('status_text')

    def window_model_showable(self, model):
        self.window_model_map[model.name] = model

    def window_model_activate(self, name):
        # Disable any current window
        current = self.window_model_current.get()

        if current != None:
            if current == name:  # Do nothing if alread active
                return
            else:
                self.window_model_map[current].window_enabled.set(False)
        # Enable new window
        self.window_model_map[name].window_enabled.set(True)
        self.window_model_current.set(name)


    def app_exit(self):
        # TODO add sanity checking to see if things need to be saved
        self.app_exit.set(True)
        
        # TODO: is it a good idea for a model to talk to the presenter directly?
    def app_open(self):
        file = self.observer.presenter.app_open()
        