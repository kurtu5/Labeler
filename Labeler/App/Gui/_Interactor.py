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

# TODO: when binds are registered, have some way to allow the presetner
# to disable them
class Interactor(MVPBase.BaseInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    # called by mvpbase_presenter.start()
    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        # now view and presenter are coupled
        self.callback_register_all()
        
    def callback_register_all(self):
        presenter = self.presenter
        
        bind1 = self.view.bind.register(
                self.view.root, '<Key>',
                lambda event: self.presenter.on_keypress(event.keysym),
                )
