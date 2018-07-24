class BaseInteractor(object):
    def __init__(self):
        self.view = None
        self.presenter = None
        self.event_groups = {}  # event_group => [event1,...],

    def start(self, presenter, view):
        self.presenter = presenter
        self.view = view
        self.event_all_register()

    def event_all_register(self):
        """ On start() register event_name()s """
        # event_add....

    def event_add(self, event_tuple, event_group = None):
        """ Register an unbount event by event group """
        event = self.event(self, *event_tuple)
        if event_group == None:
            event_group=f'event_group_{len(self.event_groups)}'
        # Create a new event_list or append
        if event_group not in self.event_groups:
            self.event_groups[event_group] = []
        self.event_groups[event_group].append(event)
        event.add()
        return event_group

    def event_group_activate(self, event_group, enable=True):
        """ Conditionally activate a event group """
        for event in self.event_groups[event_group]:
            event.activate(enable)

    def event_all_activate(self, enable=True, exclusion_list=None):
        """ Activate all event_groups not in exclusion list """
        for event_group in self.event_groups.keys():
            if exclusion_list == None or event_group not in exclusion_list:
                self.event_group_activate(event_group, enable)

 # Custom even class for Interactor
    class event:
        def __init__(self, parent_class, widget, seq, func, add=False):
            self.widget = widget
            self.seq = seq
            self.func = func
            self.add_opt = add
            self.bind_id = None
            self.is_active = None
            self._parent_class = parent_class

        def add(self):
            # Bind it
            self.bind_id = self._parent_class.view.bind.register(self.widget, self.seq, self.func, self.add_opt)
            # But then disable it until explicitly enabled
#            self.activate(self.bind_id, False)

        def activate(self, enable):
            #self.debug()
            self.is_active=enable
            self._parent_class.view.bind.activate(self.bind_id, enable)