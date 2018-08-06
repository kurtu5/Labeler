# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from PySide2.QtWidgets import QLabel, QPushButton, QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

import MVPBase

class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Setup basic window manager """

    def start(self):
        path = os.path.dirname(os.path.realpath(__file__)) + "\\"
        file = QFile(path + "options.ui")
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.page = loader.load(file)
        self.page_index = self.parent.stacked_widget.addWidget(self.page)
