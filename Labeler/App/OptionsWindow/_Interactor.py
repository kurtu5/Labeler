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

class Interactor(MVPBase.BaseInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        
    def event_all_register(self):
        self.view.e1Button.config(command=self.change_dir)
        pass
        
    def change_dir(self):
        text = self.view.e1.get()
        print(f'new dir {text}')
        self.presenter.change_dir(text)
        