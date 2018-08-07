# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)


from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMenu, QMenuBar, QAction, QLabel, QWidget, QLineEdit, QMainWindow
from PySide2.QtCore import QFile, QObject, QEvent, Signal
from PySide2 import QtCore
from PySide2.QtWidgets import QStackedWidget, QVBoxLayout

import MVPBase

class QMainWindow_S(QMainWindow):
    resized = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def resizeEvent(self, event):
        self.resized.emit()
        super().resizeEvent(event)
    
    
class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Setup basic window manager """
    # I could write this to add custom signals for custom events
    class KeyEventFilter(QObject):
        signal = Signal(QEvent)
        def __init__(self, parent, stopHere=False, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent = parent
            self.stopHere = stopHere
            self.types = []
            self.events = []

        def eventFilter(self, obj, event):
#            if (obj.objectName(), event.type()) not in self.events:
#                self.events.append((obj.objectName(), event.type()))
#                print("Some new event happened,", obj.objectName(), ",", event.type())
#            print("parent", self.parent)

            if (event.type() == QEvent.KeyPress):
#                print("emittttttttt")
                self.signal.emit(event)
            return self.stopHere

    def start(self, *a, **kw):

        path = os.path.dirname(os.path.realpath(__file__)) + "\\"
        file = QFile(path + "gui.ui")
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        loader.registerCustomWidget(QMainWindow_S)
        self.window = loader.load(file)
        

        # Global key press eventFilter.signal emits
        self.keyEvent = self.KeyEventFilter(self.parent)
        self.parent.installEventFilter(self.keyEvent)
        # self.keyEvent.signal.connect(...)

        self.stacked_widget = QStackedWidget()
#        layout = QVBoxLayout()
#        layout.addWidget(self.window.centralwidget)
        self.window.setCentralWidget(self.stacked_widget)

#        wm = QMenu("window menu")
#        self.window.menuBar().addMenu(wm)





        # Need main

        # Need status bar


#        from PySide2.QtWidgets import QPushButton
#        self.btn = QPushButton("Click Me", self.window)
#        self.btn.move(300, 200)

#        self.btn = QPushButton("Other button", self.window)
#        self.btn.move(300, 200)

#        self.label.keyPressEvent = self.keypress
#        self.window.centralwidget
#        self.window.centralwidget.addWidget(label)

#        self.window.installEventFilter(self.root)
#        self.window.eventFilter = self.eventFilter
        self.window.show()

#        self.root.geometry('1500x800+50+50')
#         self.root.wm_attributes("-topmost", 1)  # Always on top

#        self.root.lift()
#        self.root.focus_force()
#         self.current_window_class = None



    # Methods for presenter to call
    def status_text_set(self, text):
        self.window.statusbar.showMessage(text)

    def app_exit(self):
        self.parent.quit()