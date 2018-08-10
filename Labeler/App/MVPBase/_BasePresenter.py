class BasePresenter(object):
    def __init__(self, view, interactor, model, observer):
        """ Set instances for coupling """

        # Set view and interactor to couple and process events
        self.view = view
        self.interactor= interactor

        # Set model and observer to couple and process events
        self.model = model
        self.observer = observer

    def start(self):
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

    # This should be added for all showable windows
    def on_window_enable(self, enable):
        # Ingore enable unless you want to do something
        if enable == True:
            self.view.window_enable()
            self.interactor.event_all_activate(True)
            self.observer.event_all_activate(True)
        if enable == False:
            self.interactor.event_all_activate(False)
            self.observer.event_all_activate(False, ['window_enable'])
