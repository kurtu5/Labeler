# -*- coding: utf-8 -*-

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.append(path)

import tkinter as tk
import tkCustom as tkc

class ViewBase(object):
    def __init__(self, root):
        """ Create empty bind class to store toggelabe binds and set parent tk object """
        # non dynamic start
        self.bind = tkc.Bind()
        self.tk = tk
        self.tkc = tkc
        self.presenter = None
        self.root = root
        
        print("inside baseview", 'geometry' in dir(self.root), f'id(root)={id(root)}')

    def start(self):
        pass
    
#         self.bind_t('<sometype>', self.presenter_class.function)
#     def start(self, presenter):
#         pass