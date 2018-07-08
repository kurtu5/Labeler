# -*- coding: utf-8 -*-

class View(object):
    def __init__(self, root):
        """ Create empty bind class to store toggelabe binds and set parent tk object """
        # non dynamic start
        self.bind = Bind()
        self.presenter = None
        self.root = root
        
    def start(self):
        pass
    
#         self.bind_t('<sometype>', self.presenter_class.function)
#     def start(self, presenter):
#         pass