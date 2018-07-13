# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import tkinter as tk
import Gui
import MenuBar
import LabelerWindow
import TestWindow
import GenericWindow

import Images

class App(object):
    def __init__(self):
        self.root = None
   
    def start(self):
        # I don't think I need further access to instances, but I'll save them anyway
        self.root = tk.Tk()

        # Gui to handle all main window operations
        self.guiM = Gui.Model('gui')
        self.guiV = Gui.View(self.root)
        self.guiP = Gui.Presenter(self.guiV, self.guiM)
        
        # Menu for Gui
        self.menuM = MenuBar.Model('menu', {'gui': self.guiM})
        self.menuV = MenuBar.View(self.root)
        self.menuP = MenuBar.Presenter(self.menuV, self.menuM)
        
        # Testing window
        self.testM = TestWindow.Model('test', {'gui': self.guiM})
        self.testV = TestWindow.View(self.guiV.window)
        self.testP = TestWindow.Presenter(self.testV, self.testM)

        # Generic
        self.genM = GenericWindow.Model('generic', {'gui': self.guiM})
        self.genV = GenericWindow.View(self.guiV.window)
        self.genP = GenericWindow.Presenter(self.genV, self.genM)
        
        # Image labeling window
        self.imagesM = Images.Model('images')
        self.labelerM = LabelerWindow.Model('labeler', {'gui': self.guiM, 'images': self.imagesM})
        self.labelerV = LabelerWindow.View(self.guiV.window)
        self.labelerP = LabelerWindow.Presenter(self.labelerV, self.labelerM)
        
        # Config model when implemented should handle the first page to show
#        self.guiM.window_current('labeler')
        
    def run(self):
        """ Start the application """
        self.start()
      
        self.root.mainloop()