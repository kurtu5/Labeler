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
        self.state = FeatureState
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

class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.State = FeatureState
        self.selected_indexes = set()
        self.displayed_indexes = set()
        self.image_files = {}  # {index->image_file}
        self.image_features = {} # {index->Features}
        self.max_columns = None
        self.max_images = None
        self.shortcuts_labels = None
        self.label_file = None

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

         # Let guiM know im showable
        self.sib('gui').window_model_showable(self)
        self.max_columns = self.observer.event_gen('max_columns', 1)
        self.max_images = self.observer.event_gen('max_images', None)
        self.shortcuts_labels = self.observer.event_gen('shortcuts_labels', None)



    def image_feature_get(self, index, shortcut):
           if index not in self.image_features:
               return self.State.unset
           else:
               return self.image_features[index].get(shortcut)

    def image_feature_set(self, index, shortcut, state):
        if index not in self.image_features:
            self.image_features[index] = Features(self.shortcuts_labels.get())
        self.image_features[index].set(shortcut, state)

        # load from cvs and set image_labels


    def save_images(self):
        print("save current feature state")
#        self.image_features.get
        index_list = []
        features_list = []
        for index, feature in self.image_features.items():
#            print("saving images as", self.image_files[index], feature.get_all_by_name())
            index_list.append(self.image_files[index])
            features_list.append(feature.get_all_by_name())
        df = pd.DataFrame(features_list, index=index_list)
        df.to_json(self.label_file, orient='index')
        file = 'dynamicDF.csv'
        obj = None
        with open(self.label_file) as f:
            obj = json.load(f)

        outfile = open(self.label_file, "w")
        outfile.write(json.dumps(obj, indent=4, sort_keys=True))
        outfile.close()

    def load_images(self):
        self.displayed_indexes = set()
        self.sib('images').load_images()
        images = self.sib('images').image_files
#        print("imags from mode", images)
        index = 0
        max_images = self.max_images.get()
        if max_images != None and max_images != 0:
            images = images[:max_images]
        import os.path
        if os.path.isfile(self.label_file):
            df = pd.read_json(self.label_file, orient='index')
        else:
            df = pd.DataFrame()
#        print(df)

#        print("images model", self.sib('images').image_files)
        for image_file in images:
#            print("-------------image_file", index, image_file)
            if image_file in df.index:
                for shortcut, name in self.shortcuts_labels.get().items():
                    state = df.loc[image_file, name]
                    if np.isnan(state):
                        state = self.State.unset
                    self.image_feature_set(index, shortcut, state)
            else:
                for shortcut, name in self.shortcuts_labels.get().items():
                    state = self.State.unset
                    self.image_feature_set(index, shortcut, state)

            self.image_files[index] = image_file
            self.displayed_indexes.add(index)
#            self.image_features[index] = {}
            index += 1

#        print(fr"-------------images as stored in labeler {self.image_files[1]}")
#        print("load image features from csv")

    def images_display_all_with_features(self, features):
        print(f'check for featurs={features}')
        for index in self.image_files.keys():
            has_all_features = True
            print(f'image{index}', end="")
            for shortcut, label in self.shortcuts_labels.get().items():
                feature = self.image_feature_get(index, shortcut)
                print(f', {features[shortcut]} ={feature}', end="")
                if str(feature) != str(features[shortcut]):
                    print("missing", end="")
                    has_all_features = False
            print("")
            if has_all_features == True:
                self.displayed_indexes.add(index)
                print(f'image{index} has all features{features}')


    def image_select_by_status(self, index, shortcut, status):
        if status == self.image_feature_get(index, shortcut):
            self.image_select(index)

    def images_select_by_status(self, shortcut, status):
        for index in self.image_files.keys():
            self.image_select_by_status(index, shortcut, status)

    # Set if is displayed in list
    def image_display_select(self, index):
        if index not in self.displayed_indexes:
            self.displayed_indexes.add(index)

    def image_display_deselect(self, index):
        if index in self.displayed_indexes:
            self.displayed_indexes.remove(index)

    def images_display_deselect_all(self):
        self.displayed_indexes = set()
        
        
    def images_display_select_all(self):
        self.displayed_indexes = self.image_files.keys()
    
    
    # Set if is selected in list
    def image_select(self, index):
        if index not in self.selected_indexes:
            self.selected_indexes.add(index)

    def image_deselect(self, index):
        if index in self.selected_indexes:
            self.selected_indexes.remove(index)

    def images_deselect_all(self):
        self.selected_indexes = set()


    def get_all_displayable_images(self):
        images = {}
        for index in self.displayed_indexes:
#            print("index is displayable", index)
            images[index] = self.image_files[index]
        return images

    def get_selected_images(self):
        selected_images = {}
        for selected_index in self.selected_indexes:
            for index, image_file in self.image_files.items():
                if selected_index == index:
                    selected_images[index] = image_file
        return selected_images

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
