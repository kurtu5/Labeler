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


class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

         # Let guiM know im showable
        self.sib('gui').window_model_showable(self)
    
    def refresh_images(self):
        self.sib('images').load_images()
        
    def get_image(self):
        self.image_file = self.sib('images').image_file
        self.image_index = self.sib('images').image_index
    
    def get_images(self):
        return self.sib('images').images
        
    def next_image(self):
        self.sib('images').next()
        self.get_image()
        
    def prev_image(self):
        self.sib('images').prev()
        self.get_image()
        
    def status_text_update(self, text):
        self.sib('gui').status_text.set(text)
                