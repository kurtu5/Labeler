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
from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QStackedWidget, QVBoxLayout

import MVPBase

class QMainWindow_S(QMainWindow):
    resized = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resizeEvent(self, event):
        self.resized.emit()
        super().resizeEvent(event)

import time
class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Setup basic window manager """
    # I could write this to add custom signals for custom events
    class KeyEventFilter(QObject):
        KeyPress = Signal(QEvent)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.last_keypress = time.time()


        def eventFilter(self, obj, event):
            if event.type() == QEvent.KeyPress and isinstance(obj, QWindow):
#                print(obj, event.text(), "GUI---------")
                self.KeyPress.emit(event)
                return False
#            return False
            return QObject.eventFilter(self, obj, event)

    def start(self, *a, **kw):

        path = os.path.dirname(os.path.realpath(__file__)) + "\\"
        file = QFile(path + "gui.ui")
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        loader.registerCustomWidget(QMainWindow_S)
        self.window = loader.load(file)


        # Global key press eventFilter.signal emits
        self.keyEvent = self.KeyEventFilter()
        self.parent.installEventFilter(self.keyEvent)
        # self.keyEvent.signal.connect(...)

        self.stacked_widget = QStackedWidget()
#        layout = QVBoxLayout()
#        layout.addWidget(self.window.centralwidget)
        self.window.setCentralWidget(self.stacked_widget)




        self.window.show()


    # Methods for presenter to call
    def status_text_set(self, text):
        self.window.statusbar.showMessage(text)

    def app_exit(self):
        self.parent.quit()