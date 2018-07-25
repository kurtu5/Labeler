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

    def on_app_exit(self):
        self.model.app_exit()

    ### View Interactor event handlers
    def on_window_enable(self, name):
        self.model.others['gui'].window_model_activate(name)

    ### Model Observer event handlers
