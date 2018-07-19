# -*- coding: utf-8 -*-

class BaseObserver(object):
    def __init__(self):
        self._observed_name_map = {}  # name => obj
        self._observed_map = {}  # obj => callback list
        self._observer = None # observer class
        
    def callback_register_all(self):
        """ Override in derived class to define event callbacks """
        pass
#        o = self._observer
        # or o.somemethod(data)
#        self.cb1 = lambda x: print(f'x={x}')
#        self.callback_add('w1', cb1)
    

    def start(self, observer):
        self._observer = observer
        self.callback_register_all()
        
    def callback_add(self, name, func):
        if name not in self._observed_name_map.keys():
            raise Exception(f'name={name} in observer is not in use.')
        obs = self._observed_name_map[name]
        observed = self._observed_map[obs]['callBacks']
        if func in observed:
            raise Exception(f'Function: {func}, Already exists in observed.')
        observed.append(func)
        return func

    def callback_del(self, name, func):
        if name not in self._observed_name_map.keys():
            raise Exception(f'name={name} in observer is not in use.')
        obs = self._observed_name_map[name]
        observed = self._observed_map[obs]['callBacks']
        if func not in observed:
            raise Exception(f'Function: {func}, Doesn\'t exist in callBacks.')     
        observed.remove(func)

    def _callback_all_do(self, obs):
        if self._observed_map[obs]['enabled'] == True:
            for func in self._observed_map[obs]['callBacks']:
                func(obs.get())
                
    def callback_all_enable(self, obs, enable=True):
        self._observed_map[obs]['enabled'] = enable
             
    def observe_as(self, name, value = None):
        if name in self._observed_name_map.keys():
            raise Exception(f'name={name} in observer already in use.')
        obs = self._Observed(self, name, value)
        self._observed_name_map[name] = obs
        self._observed_map[obs] = {'enabled': True, 'callBacks': []}
        return obs
    
    class _Observed:
        def __init__(self, parent, name, value = None):
            self._parent = parent
            self._name = name
            self._data = value
            
        def _callback_add(self, func):
            BaseObserver.callback_add(self._parent, self._name, func)
            
        def _callback_del(self, func):
            BaseObserver.callback_del(self._parent, self._name, func)
            
        def callback_all_enable(self, enable):
            BaseObserver.callback_all_enable(self._parent, self, enable)
            
        def callback_all_do(self):
            BaseObserver._callback_all_do(self._parent, self)
        
        def set(self, data):
            self._data = data
            self.callback_all_do()

        def get(self):
            return self._data
    
        def unset(self):
            self._data = None