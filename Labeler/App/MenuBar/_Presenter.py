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
        self.start()

    def start(self):
        super().start()
        self.interactor.event_all_activate()
        self.observer.event_all_activate()

    ### Base Presenter method overrides

    ### View Interactor event handlers
    def on_window_enable(self, name):
        self.model.sib('gui').window_model_activate(name)

    def on_app_open(self):
        self.model.sib('gui').app_open()

    def on_app_exit(self):
        self.model.sib('gui').set_app_exit()

    ### Model Observer event handlers
