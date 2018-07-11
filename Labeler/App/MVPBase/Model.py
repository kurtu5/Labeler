# -*- coding: utf-8 -*-

class Model(object):
    def __init__(self, name, other_models = None):
        """ Base model stores list of related models """
        print(f'Init: {__package__}  {__class__}' )
        self.presenter = None
        self.name = name
        self.other_models = {}  # or just set to equal
        if other_models:
#             print(f'other_models={other_models}')
            for name, instance in other_models.items():
                self.add_model(name, instance)
            
    def add_model(self, name, instance):
        self.other_models[name]=instance
      
    def start(self):
        pass