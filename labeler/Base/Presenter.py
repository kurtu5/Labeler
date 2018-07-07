# -*- coding: utf-8 -*-

class Presenter(object):
    def __init__(self, view, model):
        """ Set bdirection connections with View and Model """
#         print(f'view={view}, model={model}')
        self.view = view
        self.view.presenter = self
        self.model = model
        self.model.presenter = self
        self.view.start()
        self.model.start()
        
    def start(self):

        pass
    
    
        # This is useless anyway... remove the idea of it from subclasses?
        
#         """ call start methods for model and view """
# #         print('base presenter start')
#         self.view.start()
#         self.model.start()
        
    def monitor_modelexample(self):
        self.model.monitorme.addCallback(self.makechangetoview)  