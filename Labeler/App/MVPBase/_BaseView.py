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
from tkinter import filedialog
import tkCustom as tkc

class BaseView(object):
    def __init__(self, parent):

        """ Create empty bind class to store toggelabe binds and set parent tk object """
        # non dynamic start

        self.parent = parent

    def start(self):
        pass
#        self.main = self.tk.Frame(self.root)
#        self.main.grid()
#        self.tk.Label(self.main, text="Overwrite self.main in derived class start()")

    def window_enable(self):
        self.parent.stacked_widget.setCurrentIndex(self.page_index)


    # huh... why did i put this here??!?!
    def app_open(self):
        file = filedialog.askopenfile(parent=self.root, mode='r', title='Choose file')
        return file