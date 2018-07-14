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
from tkCustom._Debug import D
 
class Presenter(MVPBase.PresenterBase):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        """ Deals with setting/unsetting binds and window management """
        self.start()
    
    def start(self):
        super().start()
 
        # Event listener to allow window close
        self.bind1_1 = self.view.bind.register(self.view.lb, '<1>', self.bt1e1)
        self.bind1_2 = self.view.bind.register(self.view.lb, '<1>', self.bt1e2, True)
        self.bind2 = self.view.bind.register(self.view.lb, '<2>', self.bt2e)
        self.bind3 = self.view.bind.register(self.view.lb, '<3>', self.bt3e)
        self.view.bind.activate_all(active=True)
        
        # Let guiM know im showable
        self.model.other_models['gui'].window_showable_add('test', self.view.main)

    def bt1e1(self, event):
        D.ebug(f'button 1 first bind')
    def bt1e2(self, event):
        D.ebug('button 1 second bind')

    def bt2e(self, event):
        D.ebug(f'disable bind1_1')
        self.view.bind.activate(self.bind1_1, False)
        
    def bt3e(self, event):
        D.ebug(f'enable bind1_1')
        self.view.bind.activate(self.bind1_1, True)

  