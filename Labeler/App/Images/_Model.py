# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import re
import MVPBase

class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = None
        self.images = None
        self.image_index = None
        self.image_file = None

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

    def load_images(self):
        path = self.sib('options').path_to_image_files
        self.path = path
        self.images = [x for x in os.listdir(f'{path}') if re.search('\.gif$|\.jpg$|\.jpeg$|\.png$',x )]
        self.image_index = 0
        self.image_file = f'{self.path}\\{self.images[self.image_index]}'
        print("images reloaded", self.images)

    def next(self):
        self.image_index = self.image_index + 1 if self.image_index < len(self.images) - 1 else 0
        self.image_file = f'{self.path}\\{self.images[self.image_index]}'
        return self.image_file

    def prev(self):
        self.image_index = self.image_index - 1 if self.image_index > 0 else len(self.images) - 1
        self.image_file = f'{self.path}\\{self.images[self.image_index]}'
        return self.image_file