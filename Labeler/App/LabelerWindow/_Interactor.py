# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)
from PySide2.QtCore import Slot
import MVPBase

class Interactor(MVPBase.BaseInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

   


    def event_all_register(self):
        """ set callbacks for events generated by view """
        v = self.view
        p = self.presenter
        add=self.event_add
        add((v.parent.window,'resized', p.on_resized), 'resized')
        add((v.keyEvent,'KeyPress', p.on_keypress))

        add((v.page.displaySelectionWidget,'display_features', p.on_select_display_features), 'select')
        add((v.page.displaySelectionWidget,'display_all', p.on_select_display_all), 'select')
        add((v.page.columns_choice,'valueChanged', p.on_columns_choice), "valueChanged")
        add((v.page.display,'imageClicked', p.on_image_clicked ), "image_signal")
        add((v.page.listWidget,'itemSelectionChanged', p.on_selection_changed), "itemSelectionChanged")

