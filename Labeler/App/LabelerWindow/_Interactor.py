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

class Interactor(MVPBase.BaseInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_items = []

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

    def itemSelectionChanged(self):
        self.event_group_blockSignals("itemSelectionChanged", True)
        self.event_group_blockSignals("image_signal", True)
        new_items = self.view.page.listWidget.selectedItems()

        # Implement in
        def isIn(item, items):
            for i in items:
                if id(item) == id(i):
                    return True
            return False

        # Find truly new items
        for new_item in new_items:
            if not isIn(new_item, self.old_items):
                index = new_item.listWidget().indexFromItem(new_item).row()
                self.presenter.model.image_select(index)

        # Find truly removed itesm
        for old_item in self.old_items:
            if not isIn(old_item, new_items):
                index = old_item.listWidget().indexFromItem(old_item).row()
                self.presenter.model.image_deselect(index)

        self.presenter.image_update()
        self.old_items = new_items
        self.event_group_blockSignals("itemSelectionChanged", False)
        self.event_group_blockSignals("image_signal", False)


    def event_all_register(self):
        """ set callbacks for events generated by view """
        self.event_add((self.view.parent.window,'resized',self.presenter.image_update), 'resized')

        self.event_add((self.view.keyEvent,'KeyPress',self.presenter.on_keypress))
#        self.event_add((self.view.keyPressEater,'keyPress',self.presenter.on_keypress))
#        self.view.page.columns_choice.valueChanged.connect(lambda e: print("spin", e))
        self.event_add((self.view.page.columns_choice,'valueChanged', self.presenter.on_columns_choice), "valueChanged")
        self.event_add((self.view.image_signal,'deselected', lambda index: self.view.image_list_setSelected(index, False) ), "image_signal")
#
#        self.event_add((self.view.page.listWidget.itemClicked,itemClicked))

        self.event_add((self.view.page.listWidget,'itemSelectionChanged',self.itemSelectionChanged), "itemSelectionChanged")
#        self.event_add((self.view.page.listWidget.itemEntered,lambda i: print("item changed")))
#        self.event_add((self.view.page.listWidget.currentItemChanged,currentItemChanged))


        p = self.presenter
        v = self.view
        add = self.event_add

        # Canvas scroll and zoom clicks
#        add((v.canvas, '<MouseWheel>', p.on_mouse_wheel), 'scroll')
#        # Left to zoom in, middle to reset and right to zoom out
#        mult = 1.5
#        add((v.canvas, '<Button 1>', lambda e: p.on_scale(mult, e)), 'zoom')
#        add((v.canvas, '<Button 2>', lambda e: p.on_scale(1.0, e)), 'zoom')
#        add((v.canvas, '<Button 3>',lambda e: p.on_scale(1/mult, e)), 'zoom2')
#
#
#        add((v.canvas, '<Key>', p.on_keyevent, True),'shortcuts')


