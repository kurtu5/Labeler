class BaseObserver(object):
    def __init__(self):
        self._observed_name_map = {}  # obs => obs_name
#        self._callback_map = {}  # obs_name => {'event_name1': {'enabled' = Bool, [cb1,...]}
        self.observer = None # observer class
        self.event_groups = {}  # event_group => [event1,...]

        # Prevent unimplemented derived method from running base method
        self._base_event_all_registered_called = False

    def start(self, observer):
        self.observer = observer
        __class__.event_all_register(self)
        try:
            self.event_all_register()
        except:
            pass

    def event_all_register(self):
        """ On start() register event_name()s """
        if self._base_event_all_registered_called == True:
            return
        self._base_event_all_registered_called = True
        pass
#        event_name('watchsizes', 'x_height', somecallback)
#        event_name('watchsizes', 'x_height', somecallback2)
#        event_name('watch2', 'x_height', somecallback2)

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

# Custom event class for Observer
    class event:
        _parent_class = None
        def __init__(self, parent_class, obs_name, func, event_name = None):
            self.obs_name = obs_name   # like widget
            self.event_name = event_name  # like seq
            self.func = func   # is func
            self.event_id = None  # like bind_id
            self.is_active = None  # used by doallcallbackstotrigger
            self._parent_class = None


        def add(self):
#            parent=__class__._parent_class
#            if self.obs_name not in parent._observed_name_map.keys():
#                raise Exception(f'obs_name={obs_name} in observer is not in use.')
            self.is_active = False
#            # Create empty callback_map for a new event_name
#        callbacks = self._callback_map[obs_name]
#        if event_name not in callbacks.keys():
#            callbacks[event_name] = {'enabled': False, 'callbacks': []}
#
#        # Add callback to event_map
#        if func in callbacks['callbacks']:
#            raise Exception(f'Function: {func}, Already exists.')
#        callbacks['callbacks'].append(func)
#
#        # Return for enabling by event_id
#        return (obs_name, event_name)

        def activate(self, enable):
            self.is_active = enable

####################
    def event_gen(self, obs_name, value = None):
        """ generate event on get(), set() """
        if obs_name in self._observed_name_map.keys():
            raise Exception(f'obs_name={obs_name} in observer already in use.')
        obs = self._Observed(self, obs_name, value)
        self._observed_name_map[obs] = obs_name
        return obs

    def _callback_all_do(self, obs):
        """ Do all callbacks of obs was get(True), set() """
        obs_name = self._observed_name_map[obs]
        for event_list in self.event_groups.values():
            for event in event_list:
                if event.obs_name == obs_name and event.is_active == True:
                    event.func(obs._data)

    class _Observed:
        def __init__(self, parent, name, value = None):
            self._parent = parent
            self._name = name
            self._data = value

        def get(self, callback_do=False):
            if callback_do == True:
                BaseObserver._callback_all_do(self._parent, self)
            return self._data

        def set(self, data, callback_do=True):
            self._data = data
            if callback_do == True:
                BaseObserver._callback_all_do(self._parent, self)