# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import json
import MVPBase

class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        self.path_to_image_files = os.path.normpath(
        "C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/")
         # Let guiM know im showable
        self.sib('gui').window_model_showable(self)
        
        self.config_file=os.path.normpath(
        "C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/config.json")
        self.config = None
        self.config_read()
        self.config_apply()
        
    def config_read(self):
        with open(self.config_file) as jsonfile:
            # `json.loads` parses a string in json format
            self.config = json.load(jsonfile)
            
        
    def config_apply(self):
        
        # Labeler
        self.sib('labeler').max_columns.set(int(self.config['LABELER']['max_columns']))
        self.sib('labeler').max_images.set(int(self.config['LABELER']['max_images']))
        self.sib('labeler').shortcuts_labels.set(dict(self.config['LABELER']['shortcuts_labels']))
        self.sib('labeler').label_file = self.config['LABELER']['labelFile']

        # Images Model
        self.sib('images').path = self.config['IMAGES']['PathToImages']
        self.sib('images').path = os.path.normpath(self.path_to_image_files)

