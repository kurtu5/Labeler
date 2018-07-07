# -*- coding: utf-8 -*-

class App(object):
    def __init__(self):
        self.root = None
   
    def start(self):
        # I don't think I need further access to instances, but I'll save them anyway
        self.root = tk.Tk()

        # Gui to handle all main window operations
        self.guiM = GuiM('gui')
        self.guiV = GuiV(self.root)
        self.guiP = GuiP(self.guiV, self.guiM)
        
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
        %gui tk
        try:
            from IPython.lib.inputhook import enable_gui
            enable_gui('tk', self.root)
        except ImportError: 
            self.root.mainloop()