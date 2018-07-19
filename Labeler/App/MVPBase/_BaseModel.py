# -*- coding: utf-8 -*-

class BaseModel(object):
    def __init__(self, name, other_models = None):
        """ Base model stores list of related models """
#        print(f'Init: Pkg:{__package__}  Cls:{__class__}' )
        self.observer = None
        self.name = name
        self.others = {}
        
        if other_models:
            for other in other_models:
                self.add_model(other)
            
    def add_model(self, other):
        self.others[other.name]=other
      
    def start(self, observer):
        self.observer = observer