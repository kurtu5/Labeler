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
import OptionsWindow
#import GenericWindow

import Images

class App(object):
    def __init__(self):
        self.root = None
   
    def start(self):
        # I don't think I need further access to instances, but I'll save them anyway
        self.root = tk.Tk()

        # Gui to handle all main window operations
        self.guiO = Gui.Observer()  # model observer callbacks to presenter set here
        self.guiM = Gui.Model('gui')
        self.guiV = Gui.View(self.root)
        self.guiI = Gui.Interactor()  # widget event callbacks to presenter set here
        self.guiP = Gui.Presenter(self.guiV, self.guiI, self.guiM, self.guiO)

        # Menu for Gui
        self.menuO = MenuBar.Observer()
        self.menuM = MenuBar.Model('menu', [self.guiM])
        self.menuV = MenuBar.View(self.root)
        self.menuI = MenuBar.Interactor()
        self.menuP = MenuBar.Presenter(self.menuV, self.menuI, self.menuM, self.menuO)
        
#        # Testing window
        self.testO = TestWindow.Observer()
        self.testM = TestWindow.Model('test', [self.guiM])
        self.testV = TestWindow.View(self.guiV.window)
        self.testI = TestWindow.Interactor()
        self.testP = TestWindow.Presenter(self.testV, self.testI, self.testM, self.testO)
#
#        # Generic
#        self.genM = GenericWindow.Model('generic', {'gui': self.guiM})
#        self.genV = GenericWindow.View(self.guiV.window)
#        self.genP = GenericWindow.Presenter(self.genV, self.genM)
        
        # Image labeling window
        self.imagesM = Images.Model('images')
        self.labelerO = LabelerWindow.Observer()
        self.labelerM = LabelerWindow.Model('labeler', [self.guiM, self.imagesM])
        self.labelerV = LabelerWindow.View(self.guiV.window)
        self.labelerI = LabelerWindow.Interactor()
        self.labelerP = LabelerWindow.Presenter(self.labelerV, self.labelerI, self.labelerM, self.labelerO)

        # Options labeling window
        self.optionsO = OptionsWindow.Observer()
        self.optionsM = OptionsWindow.Model('options', [self.guiM, self.imagesM])
        self.optionsV = OptionsWindow.View(self.guiV.window)
        self.optionsI = OptionsWindow.Interactor()
        self.optionsP = OptionsWindow.Presenter(self.optionsV, self.optionsI, self.optionsM, self.optionsO)
                
        # Config model when implemented should handle the first page to show
#        self.guiM.window_current('labeler')
        
    def run(self):
        """ Start the application """
        self.start()
      
        self.root.mainloop()