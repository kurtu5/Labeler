# -*- coding: utf-8 -*-

class BasePresenter(object):
    def __init__(self, view, interactor, model, observer):
        """ Set instances for coupling """
#        print(f'Init: Pkg:{__package__}  Cls:{__class__}' )
        
        # Set view and interactor to couple and process events
        self.view = view
        self.interactor= interactor
        
        # Set model and observer to couple and process events
        self.model = model
        self.observer = observer
        
    def start(self):
#        print("PPPPPPPPPPP P, M, V, I, O", self, self.model, self.view,self.interactor,self.observer)
        """ Start M,V and P and then couple them """
        # Start view 
        # Since it can generate events, it doesn't need
        # to know about the Interactor instance
        self.view.start()
        # Finish coupling view events to presenter callbacks
        self.interactor.start(self, self.view)
        
        # Start model
        # Since it can't generate events, give it an Observer
        # instance to do so.
        self.model.start(self.observer)
        # Finish Coupling model events to presenter callbacks
        self.observer.start(self) 
        
        # Derived Presenter will then start()