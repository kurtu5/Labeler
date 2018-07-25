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
#import MVPBase
#
#class Model(MVPBase.BaseModel):
class Model():
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.path = None
        self.index = None
        self.images = None
        self.current_image = None

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

    def load_images(self, path):
        self.path = path
        self.images = [x for x in os.listdir(f'{path}') if re.search('\.gif$|\.jpg$|\.jpeg$|\.png$',x )]
        self.index = 0
        self.current_image = f'{self.path}\\{self.images[self.index]}'

    def next(self):
        self.index = self.index + 1 if self.index < len(self.images) - 1 else 0
        self.current_image = f'{self.path}\\{self.images[self.index]}'
        return self.current_image

    def prev(self):
        self.index = self.index - 1 if self.index > 0 else len(self.images) - 1
        self.current_image = f'{self.path}\\{self.images[self.index]}'
        return self.current_image