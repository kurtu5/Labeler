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
Observable = MVPBase.ObservableBase

class Presenter(MVPBase.PresenterBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Deals with setting/unsetting binds and window management """
        self.start()
        self.window_current = Observable()
        self.window_current.addCallback(self.window_show)
        self.model.statustext = Observable()
        self.model.statustext.addCallback(self.status_text)
    
    def start(self):
        super().start()
        # Event listener to allow window close
        bind1 = self.view.bind.register(self.view.root, '<Key>', self.keypress)
        self.view.bind.activate_all(active=True)

    
    def window_show(self, widget):
#         print(f'window_show for {widget}')
        widget.tkraise()
    
    def status_text(self, text):
        self.view.statustext.config(text=text)
        
    # Event handlers
    def keypress(self, event):
#         print('esc pressed')
        """ Handle top level keyboard shortcuts then pass any to the current window """
        #         print("mykeypressg", event, event.state)
        if ( event.keysym == 'Escape'):
            self.closeapp()
            
    def closeapp(self):
        self.view.root.destroy()