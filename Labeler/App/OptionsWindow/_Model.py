# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import configparser
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
        "C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/config.ini")
        self.config = configparser.ConfigParser()
        self.config_read()
        self.config_apply()
        
    def config_read(self):
        self.config.read(self.config_file)
        
    def config_apply(self):
        
        # Labeler
        self.sib('labeler').max_columns.set(int(self.config['LABELER']['max_cols']))
        # Images Model
        self.sib('images').path = self.config['IMAGES']['PathToImages']
        self.sib('images').path = os.path.normpath(self.path_to_image_files)
        self.sib('images').max = int(self.config['IMAGES']['max'])

