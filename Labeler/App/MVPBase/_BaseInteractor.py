class BaseInteractor(object):
    def __init__(self):
        self.view = None
        self.presenter = None
        self.event_groups = {}  # event_group => [event1,...],

        # Prevent unimplemented derived method from running base method
        self._base_event_all_registered_called = False

    def start(self, presenter, view):
        self.presenter = presenter
        self.view = view
        __class__.event_all_register(self)
        self.event_all_register()

    def event_all_register(self):
        """ On start() register event_name()s """
        if self._base_event_all_registered_called == True:
            return
        self._base_event_all_registered_called = True
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
        def __init__(self, parent_class, signal, slot):
            self.signal = signal
            self.slot = slot
            self.is_active = None
            self._parent_class = parent_class

        def add(self):
            # Bind it
#            self.bind_id = self._parent_class.view.bind.register(self.widget, self.seq, self.func, self.add_opt)
            # But then disable it until explicitly enabled
            self.is_active = False

        def activate(self, enable):
            if enable == True:
                self.signal.connect(self.slot)
                self.is_active = enable
            else:
                self.signal.disconnect(self.slot)
                self.is_active = enable
