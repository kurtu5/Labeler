# -*- coding: utf-8 -*-
import tkinter as tk

#from Gui.Model import Model
import MVPBase
from Gui.Model import Model

class App(object):
    def __init__(self):
        self.root = None
   
    def start(self):
        # I don't think I need further access to instances, but I'll save them anyway
        self.root = tk.Tk()

        # Gui to handle all main window operations
        self.guiM = GuiModel('gui')
        self.guiV = GuiView(self.root)
        self.guiP = GuiPresenter(self.guiV, self.guiM)
        
        # Menu for Gui
        self.menuM = MenuBarM('menu', {'gui': self.guiM})
        self.menuV = MenuBarV(self.root)
        self.menuP = MenuBarP(self.menuV, self.menuM)
        
        # Testing window
        self.testM = TestM('test', {'gui': self.guiM})
        self.testV = TestV(self.guiV.window)
        self.testP = TestP(self.testV, self.testM)
        
        # Image labeling window
        self.imagesM = ImagesM('images')
        self.labelerM = LabelerM('labeler', {'gui': self.guiM, 'images': self.imagesM})
        self.labelerV = LabelerV(self.guiV.window)
        self.labelerP = LabelerP(self.labelerV, self.labelerM)
        
        # Config model when implemented should handle the first page to show
        self.guiM.window_current('labeler')
        
    def run(self):
        """ Start the application """
        self.start()
        self.root.mainloop()