# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import pandas as pd
import json
import numpy as np
import MVPBase

class FeatureState:
    yes = 1
    no = -1
    unset = 0
    unsure = 10

class Features:
    def __init__(self, shortcuts_labels):
        self.State = FeatureState
        self.feature_states = {}
        self.shortcuts_labels = shortcuts_labels

    def set(self, shortcut, state):
        if shortcut not in self.shortcuts_labels:
            raise Exception("not a valid shortcut")
        # check if state is valid?
        self.feature_states[shortcut] = state

    def get(self, shortcut):
        if shortcut not in self.shortcuts_labels:
            raise Exception("not a valid shortcut")
        if shortcut not in self.feature_states:
            return self.state.unset
        else:
            return self.feature_states[shortcut]

    def get_all_by_name(self):
        """ r """
        nameStates = {}
        for shortcut, feature_name in self.shortcuts_labels.items():
            state = self.get(shortcut)
            nameStates[feature_name] = state
        return nameStates

class Image:
    def __init__(self):
        self._displayed = None
        self._selected = None
        self._selected = None
        self._features = None
    
    def isDisplayed(self):
        return self._displayed
    def setDisplayed(self, displayed):
        self._displayed = displayed

    def isSelected(self):
        return self._selected
    def setSelected (self, selected):
        self._selected = status
        
    def getFilename(self):
        return self._selected
    def setFilename(self, filename):
        self._selected = filename
        
    def getFeatures(self):
        return self._features
    def setFeatures(self, features):
        self._features = features
        
    def getFeature(self, shortcut):
        return self._features.get(shortcut)
    def setFeature(self, shortcut, feature):
        self._features.set(shortcut, feature)
        
    def hasFeature(self, shortcut, feature):
        if self._features[shortcut] == feature:
            return True
        else:
            return False
        
    def hasAllFeatures(self, features):
        has_all_features = True
        for shortcut, feature in features.items():
            if not self.has_feature(shortcut, feature):
                has_all_features = False
        return has_all_features
    
    
class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_columns = None
        self.max_images = None
        self.shortcuts_labels = None
        self.label_file = None
        self.images = {}   # index := Image
        self.State = FeatureState


    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

         # Let guiM know im showable
        self.sib('gui').window_model_showable(self)
        self.max_columns = self.observer.event_gen('max_columns', 1)
        self.max_images = self.observer.event_gen('max_images', None)
        self.shortcuts_labels = self.observer.event_gen('shortcuts_labels', None)

        # load from cvs and set image_labels


    def save_images(self):
        print("save current feature state")
#        self.image_features.get
        index_list = []
        features_list = []
        for index, image in self.images.items():
#            print("saving images as", self.image_files[index], feature.get_all_by_name())
            index_list.append(image.getFilename())
            features_list.append(image.getFeatures().get_all_by_name())
        df = pd.DataFrame(features_list, index=index_list)
        df.to_json(self.label_file, orient='index')

        obj = None
        with open(self.label_file) as f:
            obj = json.load(f)

        outfile = open(self.label_file, "w")
        outfile.write(json.dumps(obj, indent=4, sort_keys=True))
        outfile.close()

    def load_images(self):
        self.sib('images').load_images()
        image_files = self.sib('images').image_files
        max_images = self.max_images.get()
        if max_images != None and max_images != 0:
            image_files = image_files[:max_images]
            
        # Open labels
        import os.path
        if os.path.isfile(self.label_file):
            df = pd.read_json(self.label_file, orient='index')
        else:
            df = pd.DataFrame()

        index = 0
        for image_file in image_files:
            image = Image()
            image.setFilename(image_file)
            image.setDisplayed(True)
            image.setSelected(False)
            image.setFeatures(Features())

            for shortcut, name in self.shortcuts_labels.get().items():
                if image_file in df.index:
                    state = df.loc[image_file, name]
                    if np.isnan(state):
                        state = self.State.unset
                else:
                    state = self.State.unset
                image.setFeature(shortcut, state)

            self.images[index] = image
            index += 1

#        print(fr"-------------images as stored in labeler {self.image_files[1]}")
#        print("load image features from csv")

    def images_display_all_with_features(self, features):
        print(f'check for featurs={features}')
        images = self.images
        for index, image in images.items():
            if image.hasAllFeatures(features) == True:
                self.images[index].setDisplayed(True)
                print(f'image{index} has all features{features}')


    def image_select_first_displayable(self):
        index = self.get_first_displayable_index()
        if index != None:
            self.model.image_select(index)
            
    def image_select_by_status(self, index, shortcut, status):
        if self.images[index].hasFeature(shortcut, feature):
            self.images[index].setSelected(True)

    def images_select_by_status(self, shortcut, status):
        images = self.images
        for index, image in self.image.items():
            if image.hasFeature(shortcut, status) == True:
                images[index].setSelected(True)

    # Set if is displayed in list
    def image_display_select(self, index):
        self.images[index].setSelected(True)

    def image_display_deselect(self, index):
        self.images[index].setDisplayed(False)


    def images_display_deselect_all(self):
        images = self.images
        for index, image in images.items():
            self.images[index].setDisplayed(False)    
        
    def images_display_select_all(self):
        images = self.images
        for index, image in images.items():
            self.images[index].setDisplayed(True)    
    
    # Set if is selected in list
    def image_select(self, index):
        self.images[index].setSelected(True)

    def image_deselect(self, index):
        self.images[index].setSelected(False)


    def images_deselect_all(self):
        images = self.images
        for index, image in images.items():
            self.images[index].setSelected(False)   

    def get_all_displayable_images(self):
        images = {}
        for index, image in self.images.items():
            if image.getDisplayed() == True:
                images[index] = image
        return images
    
    def get_first_displayable_index(self):
        for index, image in self.images.items():
            if image.getDisplayed() == True:
                return index
        return None

    def get_selected_images(self):
        images = {}
        for index, image in self.images.items():
            if image.getSelected() == True:
                images[index] = image
        return images

    # Probably don't need these.  USe the listWidget select to page through images
    def image_select_next(self):
        selected = self.selected_indexes
        if selected == {}:
            index = 1
        else:
            last = list(selected)[-1]
            index = last + 1 if last < len(self.image_files) -1 else 0
        self.image_select(index)

    def image_select_prev(self):
        selected = self.selected_indexes
        if selected == {}:
            index=len(self.image_files) - 1
        else:
            first = list(selected)[-1]
            index = first - 1 if first > 0 else len(self.image_files) - 1
        self.image_select(index)

#    def get_image(self):
#        self.image_file = self.sib('images').image_file
#        self.image_index = self.sib('images').image_index
#
#    def get_images(self):
#        images = []
#        for image in self.sib('images').images:
#            images.append(self.sib('images').path + "\\" + image)
#        return images
#
#    def indexed_image(self, index):
#        self.sib('images').indexed(index)
#        self.get_image()
#
#    def next_image(self):
#        self.sib('images').next()
#        self.get_image()
#
#    def prev_image(self):
#        self.sib('images').prev()
#        self.get_image()

    def status_text_update(self, text):
        self.sib('gui').status_text.set(text)
