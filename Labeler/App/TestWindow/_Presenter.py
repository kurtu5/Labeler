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
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        """ Deals with setting/unsetting binds and window management """
        self.start()

    def start(self):
        super().start()
         # Let guiM know im showable
        self.model.others['gui'].window_model_showable(self.model)

    ### View Interactor event handlers

    ### Model Observer event handlers
