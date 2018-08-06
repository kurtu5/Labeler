# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import MVPBase


from PySide2.QtWidgets import QLabel, QPushButton, QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):

            # Since I have default implemetations for showable pages, do this in base?
            path = os.path.dirname(os.path.realpath(__file__)) + "\\"
            file = QFile(path + "test.ui")
            file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.page = loader.load(file)
            self.page_index = self.parent.stacked_widget.addWidget(self.page)

