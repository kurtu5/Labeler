# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from PySide2.QtTest import QTest
from PySide2.QtCore import QEvent, Qt, Slot
from PySide2 import QtGui
from PySide2.QtWidgets import QApplication
import MVPBase

class Presenter(MVPBase.BasePresenter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_scale = 1.0
        self.scale = self.default_scale
        self.scale_xloc = 0  # TODO maybe shove these into view
        self.scale_yloc = 0
        self.image_index = None
        self.old_selections = []

        self.start()

    def start(self):
        super().start()
        # TODO This stuff should be pulled from model and set to model
        self.shortcuts_labels = {"q": "feat1", "w": "feat2", "e": "feat3", "r": "other"}
        self.labels = {}  # TODO When controller loads image, should set this from csv

        self.interactor.event_all_activate(False, ['resized'])
        self.observer.event_all_activate(False, ['window_enable'])


## TODO where do these belong?
    def image_update(self):
        self.interactor.event_group_blockSignals("itemSelectionChanged", True)
        self.interactor.event_group_blockSignals("image_signal", True)
        selected_images = self.model.get_selected_images()
#        print("show images=", images)
        self.view.images_load(selected_images)
        self.interactor.event_group_blockSignals("itemSelectionChanged", False)
        self.interactor.event_group_blockSignals("image_signal", False)

        # Update labelerwidget to reflect current features
        self.view.page.labelerWidget.set_shortcuts_labels(self.model.shortcuts_labels.get())

        features = {}
        for shortcut in self.model.shortcuts_labels.get().keys():
            features[shortcut] = None
#        print("unset features are", features)
        # Go through all selected and see if they have different features for each feature
        for index, image in selected_images.items():
            for shortcut, feature in features.items():
                val = image.getFeature(shortcut)
#                print('its in model as and features as',feature, val, features[feature])
                if features[shortcut] == None:
                    features[shortcut] = val
                elif features[shortcut] != val:
                    features[shortcut] = 'conflicting'
#            print("     features is now", features)

#        print('features loop')
        for shortcut, feature in features.items():
            if features[shortcut] == None:
                features[shortcut] = self.model.State.unset
#            print('features', feature, features[feature])
            self.view.page.labelerWidget.set_shortcuts_status(shortcut, features[shortcut] )


        # Update status string
#        status_text = f'index: {self.model.image_index} image: {self.model.image_file} scale: {self.scale:.2f}'
#        self.model.status_text_update(status_text)

#        self.view.block_selected = True
#        self.view.image_list_setSelected(self.model.image_index)
#        self.view.block_selected = False

#        image_count = len(self.model.get_images())
#        self.view.image_listbox.select_clear(0, image_count)
#        self.view.image_listbox.see(self.model.image_index)

#        self.view.image_listbox.select_set(self.model.image_index)
#        self.view.image_update(self.scale, self.scale_xloc, self.scale_yloc)

    def image_list_update(self):
        images = self.model.get_all_displayable_images()

        self.view.image_list_update(images, self.model.shortcuts_labels.get())

## deal with labeling shortcuts

    def label(self, key, has_feature = None):
        """ set label on image and update view """
        # Cycle through labels
        if has_feature == None:
            cycle = [-1, 0, 1]
            if key not in self.labels:
                current = 0
            else:
                current = self.labels[key]
            has_feature = cycle[(cycle.index(current)+1)%len(cycle)]
        # Set
        self.labels[key] = has_feature
        self.view.set_label_widget(key, has_feature)


    ### Base Presenter method overrides
    def on_window_enable(self, enable):
        super().on_window_enable(enable)
        if enable == True:
            self.refresh_images()
            self.on_reconfigure()
        if enable == False:
            print("Skipping model save images")
           # self.model.save_images()

# TODO: remove observer?  reconfig everytime page loads
#        if enable == False:
#            self.observer.event_group_activate('reconfigure', True)

    def refresh_images(self):
        self.on_reconfigure()
        self.model.load_images()
        self.model.image_select_first_displayable()
        self.scale = self.default_scale
        self.image_update()
        self.image_list_update()
#            self.view.canvas.focus_set()


#            self.view.image_list_set(items)

    ### View Interactor event handlers
    
    def on_resized(self):
        self.image_update()

    def on_image_clicked(self, index, event):
        self.view.page.listWidget.setSelected(index, False)

    def on_select_display_features(self, features):
        self.model.images_deselect_all()
        self.model.images_display_deselect_all()
        self.model.images_display_all_with_features(features)
        print("call select first")
        self.model.image_select_first_displayable()
        self.model.debug_dsa("---current selection--------")
        self.image_list_update()
        self.image_update()
        print("done")
        
    def on_select_display_all(self):
        self.model.images_display_select_all()
        self.model.images_deselect_all()
        self.model.image_select_first_displayable()
        self.image_list_update()
        self.image_update()

    def on_columns_choice(self, choice):
        self.view.max_columns_choice(choice)
        self.image_update()

    def on_scale(self, scale, event):
        if scale == 1:
            self.scale = 1.0
        else:
            self.scale *= scale;
            self.scale_xloc = event.x
            self.scale_yloc = event.y
        self.image_update()

    def on_scroll(self, amount):
        self.view.scroll(amount)

    def on_mouse_wheel(self, event):
        amount = 0
        # Deal with linux and windows events
        if event.num == 5 or event.delta == -120:
            amount += 1
        elif event.num == 4 or event.delta == 120:
            amount -= 1
        self.on_scroll(amount)

    def on_keypress(self, event):
        State = self.model.State
        for shortcut in self.model.shortcuts_labels.get().keys():
            qtkey = QTest.asciiToKey(shortcut)
            if event.key() == qtkey and not event.isAutoRepeat():
#
                modifiers = event.modifiers()
                if modifiers == Qt.ShiftModifier:
                    self.update_features(shortcut, feature = State.no)
                elif modifiers ==  Qt.ControlModifier:
                    self.update_features(shortcut, feature = State.unset)
                elif modifiers == ( Qt.ControlModifier |
                                    Qt.ShiftModifier):
                    self.update_features(shortcut, feature = State.unsure)
#                elif modifiers == ( Qt.AltModifier):
#                    self.update_features(shortcut, toggle = True)
                else:
                    self.update_features(shortcut, feature = State.yes)
        if event.key() == Qt.Key_Space:
#            print("deselect all items in list")
#            self.model.images_deselect_all()
#            print("model selected images")
#            self.model.debug_dsa()
            pass

        return

#        if event.keysym == 'space' or event.keysym == 'Down':
#            self.on_scroll(2)
#        if event.keysym == 'Up':
#            self.on_scroll(-2)
        if event.key() == Qt.Key_Right:
#            self.scale = self.default_scale
            self.model.next_image()
            self.image_update()
        if event.key() == Qt.Key_Left:
#            self.scale = self.default_scale
            self.model.prev_image()
            self.image_update()
        # Pass to shortcut to check if one was used
#        self.on_keyshortcut(event)


    def update_features(self, shortcut, feature = None, toggle = None):
        """ set feature on image(s) and update view """

        # Cycle through labels
#        if toggle == True:
#            cycle = [-1, 0, 1]
#            if key not in self.labels:
#                current = 0
#            else:
#                current = self.labels[key]
#            has_feature = cycle[(cycle.index(current)+1)%len(cycle)]
        # Set
#        self.labels[key] = has_feature

        selected_images = self.model.get_selected_images()
        length = len(selected_images)
        if length == 0:
            return

        for item in self.view.page.listWidget.selectedItems():
            item.set_shortcuts_status(shortcut, feature)
            self.model.images[item.index].setFeature(shortcut, feature)

        # graphicsitems suck and i should replace them?
#        for i in range (0,self.view.multiple_image_layout.count()):
#                graphicsitem = self.view.multiple_image_layout.itemAt(0)
#                graphicsitem.label()
#        for graphicsitem in self.multiple_image_layout
        self.view.page.labelerWidget.set_shortcuts_status(shortcut, feature)

    def on_selection_changed(self):
        self.interactor.event_group_blockSignals("itemSelectionChanged", True)
        self.interactor.event_group_blockSignals("image_signal", True)
        new_selections = self.view.page.listWidget.selectedItems()

        # Implement in
        def isIn(item, items):
            for i in items:
                if id(item) == id(i):
                    return True
            return False

        # Find truly new items
        for new_selection in new_selections:
            if not isIn(new_selection, self.old_selections):
                index = new_selection.listWidget().indexFromItem(new_selection).row()
                self.model.image_select(index)

        # Find truly removed itesm
        for old_selection in self.old_selections:
            if not isIn(old_selection, new_selections):
                index = old_selection.listWidget().indexFromItem(old_selection).row()
                self.model.image_deselect(index)

        self.image_update()
        self.old_selections = new_selections
        self.interactor.event_group_blockSignals("itemSelectionChanged", False)
        self.interactor.event_group_blockSignals("image_signal", False)
        self.model.debug_dsa("sections after on selection changed")


    ### Model Observer event handlers
    def on_reconfigure(self):
        """ Apply new configuration options """
        print("reconfigure")
        self.view.page.labelerWidget.set_shortcuts_labels(self.model.shortcuts_labels.get())
        self.view.page.displaySelectionWidget.set_shortcuts_labels(self.model.shortcuts_labels.get())
        self.on_columns_choice(self.model.max_columns.get())
        self.view.max_images = self.model.max_images.get()
        self.model.images_display_select_all()
