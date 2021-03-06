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

class Observer(MVPBase.BaseObserver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

    def event_all_register(self):
        self.event_add(('max_columns', lambda x: self.presenter.on_reconfigure()), 'reconfigure')
        self.event_add(('max_images', lambda x: self.presenter.on_reconfigure()), 'reconfigure')
