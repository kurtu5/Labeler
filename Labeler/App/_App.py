#import tkinter as tk
#import Labeler.App.Gui as Gui
from .Gui import *
#from .MenuBar import *
#from .TestWindow import *
#from .Images import *
#from .LabelerWindow import *

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
        
        # Image labeling window
        self.imagesM = Images.Model('images')
        self.labelerM = LabelerWindow.Model('labeler', {'gui': self.guiM, 'images': self.imagesM})
        self.labelerV = LabelerWindow.View(self.guiV.window)
        self.labelerP = LabelerWindow.Presenter(self.labelerV, self.labelerM)
        
        # Config model when implemented should handle the first page to show
        self.guiM.window_current('labeler')
        
    def run(self):
        """ Start the application """
        self.start()
        self.root.mainloop()