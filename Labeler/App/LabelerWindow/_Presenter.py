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
from PySide2.QtCore import QEvent, Qt
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
        images = self.model.get_all_images()

#            print(images)
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
            self.reconfigure()
# TODO: remove observer?  reconfig everytime page loads
#        if enable == False:
#            self.observer.event_group_activate('reconfigure', True)

    def refresh_images(self):
        self.model.load_images()

        self.scale = self.default_scale

        self.image_update()
        self.image_list_update()
#            self.view.canvas.focus_set()


#            self.view.image_list_set(items)

    ### View Interactor event handlers
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
        if event.type() != QEvent.Type.KeyPress:
            return
            key = event.key()
            # Qt.Key doc for keycodes
#        print("In Labeler key=", event.text())
#        print(type(event))
#        return
        for shortcut in self.model.shortcuts_labels.get().keys():
            qtkey = QTest.asciiToKey(shortcut)
            if event.key() == qtkey and not event.isAutoRepeat():
#                print("----------------------")
#
#                for i in  ['modifiers', 'key', 'text', 'type', 'hasExtendedInfo', 'nativeScanCode', 'nativeVirtualKey','nativeModifiers']:
#                    print(f'{i}=', end="")
#                    try:
#                        print(eval(f'event.{i}()'))
#                    except:
#                        print("Not defined")
                        
        # set if only the key was pressed
        # control = no feature
        # alt = toggle
        # shift= unknown feature
                modifiers = event.modifiers()
                # Unknown 0
                if modifiers == Qt.ShiftModifier:
#                    print('Shift')
                    self.set_labels(shortcut, has_feature = 0)
                # No Feature -1  
                elif modifiers ==  Qt.ControlModifier:
#                    print('Control')
                    self.set_labels(shortcut, has_feature = -1)

                # Unsure -10
                elif modifiers == ( Qt.ControlModifier |
                                    Qt.ShiftModifier):
#                    print('Control+Shift')
                    self.set_labels(shortcut, has_feature = -10)

                # Toggle 
                elif modifiers == ( Qt.AltModifier):
#                    print('Alt')
                    self.set_labels(shortcut, toggle = True)
                # Has feature 1
                else:
#                    print('Vanilla')
                    self.set_labels(shortcut, has_feature = 1)


        return

#        if event.keysym == 'space' or event.keysym == 'Down':
#            self.on_scroll(2)
#        if event.keysym == 'Up':
#            self.on_scroll(-2)
        if key == Qt.Key_Right:
#            self.scale = self.default_scale
            self.model.next_image()
            self.image_update()
        if key == Qt.Key_Left:
#            self.scale = self.default_scale
            self.model.prev_image()
            self.image_update()
        # Pass to shortcut to check if one was used
#        self.on_keyshortcut(event)


    def set_labels(self, feature, has_feature = None, toggle = None):
        """ set label on image and update view """
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
        for item in self.view.page.listWidget.selectedItems():
            print("item=",item)
            item.set_shortcuts_status(feature, has_feature)
        self.view.page.labelerWidget.set_shortcuts_status(feature, has_feature)



    def on_row_changed(self, row):
#        selected = self.view.page.listWidget.item(row).isSelected()
#        print(f'the item at {row} is {selected} selected')
        self.model.image_select(row)
        self.image_update()

    ### Model Observer event handlers
    def reconfigure(self):
        """ Apply new configuration options """
        self.view.page.labelerWidget.set_shortcuts_labels(self.model.shortcuts_labels.get())
        self.on_columns_choice(self.model.max_columns.get())
        self.view.max_images = self.model.max_images.get()