# -*- coding: utf-8 -*-

class BaseModel(object):
    def __init__(self, name, other_models = None):
        """ Base model stores list of related models """
#        print(f'Init: Pkg:{__package__}  Cls:{__class__}' )
        self.observer = None
        self.name = name
        self.other_models = {}  # or just set to equal
        if other_models:
#             print(f'other_models={other_models}')
            for name, instance in other_models.items():
                self.add_model(name, instance)
            
    def add_model(self, name, instance):
        self.other_models[name]=instance
      
    def start(self, observer):
        self.observer = observer