# -*- coding: utf-8 -*-

class Bind(object):
    """ Wraps tkinter bind to allow easy toggleing of bind active state """
    def __init__(self):
        self.registry = {}

    def register(self, parent, sequence, func, add=False):
        """ store desired binds in registry """

        bind_id = f'bind_{len(self.registry)}'
        self.registry[bind_id]=[parent, sequence, func, add, None, False]
#        self.activate(bind_id, True)
        return bind_id

    def isactive(self, bind_id):
        return self.registry[bind_id][5]

    def activate(self, bind_id, active):
        parent, sequence, func, add, funcid, activeV = self.registry[bind_id]
        if active == True and activeV != True:
#             D.ebug('---activating')
            funcid = self.__bind(parent, sequence, func, add)
            self.registry[bind_id][4] = funcid
            self.registry[bind_id][5] = True
        elif active == False and activeV == True:
#             D.ebug('---deactivating')

            self.__unbind(parent, sequence, funcid)
            self.registry[bind_id][4] = None
            self.registry[bind_id][5] = False

    def activate_all(self, active):
        """ activate or deactivate registered binds """
        for bind_id in self.registry.keys():
            self.activate(bind_id, active)

    def toggle_active(self, state):
        """ toggle any active to off so they can be toggled back on """
        pass


    def __bind(self, parent, sequence, func, add=None):
        # For now ignore the add=False default and set to True for all
        funcid = parent.bind(sequence, func, True)
        return funcid

    def __unbind(self, parent, sequence, funcid=None):
        '''  Workaround tkinter to allow deleting by funcid only
        See:
        http://stackoverflow.com/questions/6433369/
        deleting-and-changing-a-tkinter-event-binding-in-python
        '''

        if not funcid:
            self.tk.call('bind', parent._w, sequence, '')
            return
        func_callbacks = parent.tk.call('bind', parent._w, sequence, None).split('\n')
        new_callbacks = [l for l in func_callbacks if l[6:6 + len(funcid)] != funcid]
        parent.tk.call('bind', parent._w, sequence, '\n'.join(new_callbacks))
        parent.deletecommand(funcid)