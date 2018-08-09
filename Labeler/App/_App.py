# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

#import tkinter as tk
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer

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
#        self.root = tk.Tk()
        self.parent = QtWidgets.QApplication([])


        # Gui to handle all main window operations
        self.guiO = Gui.Observer()  # model observer callbacks to presenter set here
        self.guiM = Gui.Model('gui')
        self.guiV = Gui.View(self.parent)
        self.guiI = Gui.Interactor()  # widget event callbacks to presenter set here
        self.guiP = Gui.Presenter(self.guiV, self.guiI, self.guiM, self.guiO)

        # Menu for Gui
        self.menuO = MenuBar.Observer()
        self.menuM = MenuBar.Model('menu')
        self.menuV = MenuBar.View(self.guiV)
        self.menuI = MenuBar.Interactor()
        self.menuP = MenuBar.Presenter(self.menuV, self.menuI, self.menuM, self.menuO)

#        # Testing window
        self.testO = TestWindow.Observer()
        self.testM = TestWindow.Model('test')
        self.testV = TestWindow.View(self.guiV)
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
        self.labelerM = LabelerWindow.Model('labeler')
        self.labelerV = LabelerWindow.View(self.guiV)
        self.labelerI = LabelerWindow.Interactor()
        self.labelerP = LabelerWindow.Presenter(self.labelerV, self.labelerI, self.labelerM, self.labelerO)

#         Options window
        self.optionsO = OptionsWindow.Observer()
        self.optionsM = OptionsWindow.Model('options')
        self.optionsV = OptionsWindow.View(self.guiV)
        self.optionsI = OptionsWindow.Interactor()
        self.optionsP = OptionsWindow.Presenter(self.optionsV, self.optionsI, self.optionsM, self.optionsO)

        # Make labeler the default window
        self.guiM.window_model_activate('labeler')

    def run(self):
        """ Start the application """
        self.start()

#        self.root.mainloop()

        # https://stackoverflow.com/questions/5160577/ctrl-c-doesnt-work-with-pyqt
        #   In case the app doesnt display and show an X button to close
        import signal
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        #https://machinekoder.com/how-to-not-shoot-yourself-in-the-foot-using-python-qt/
        # This only works if you do the sys.exit(...exec_) thing
        #but not inside the class.. maybe in main or something
#        self.timer = QTimer()
#        self.timer.timeout.connect(lambda: print("python event processing"))
#        self.timer.start(100)
        def except_hook(cls, exception, traceback):
            sys.__excepthook__(cls, exception, traceback)
        
 

        import sys
#        sys.excepthook = except_hook
#        sys.exit(self.root.exec_())
        try:
            self.parent.exec_()
        except:
            raise Exception("abnormal termination")
        print("program ended normally")