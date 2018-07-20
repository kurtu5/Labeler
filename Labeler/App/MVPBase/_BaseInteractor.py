# -*- coding: utf-8 -*-

class BaseInteractor(object):
    def __init__(self):
        self.view = None
        self.presenter = None
        self.binds = {}

    def start(self, presenter, view):
        self.presenter = presenter
        self.view = view
        
    def bind_as(self, bind_name, widget, seq, func, add=False):
        bind_id = self.view.bind.register(widget, seq, func)
        if bind_name == None:
            bind_name=bind_id
        self.binds[bind_name] = bind_id
        
    def bind_activate(self, bind_name, enable=True):
        self.view.bind.activate(self.binds[bind_name], enable)
        
    def binds_disable(self, exclusion_list=None):
        _binds_activate(False, exclusion_list)
        
    def binds_enable(self, exclusion_list=None):
        _binds_activate(False, exclusion_list)
        
    def binds_register(self):
        
    
    def _binds_activate(self, enable, exclusion_list):
        for bind_name, bind_id in self.binds.items():
            if exclusion_list == None or bind_name not in exclusion_list:
                self.bind_activate(bind_name, enable)
