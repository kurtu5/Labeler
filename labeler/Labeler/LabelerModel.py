# -*- coding: utf-8 -*-

class LabelerM(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def start(self):
#         print('labeler i should tell gui that im showable'
        self.other_models['images'].load_images('dildo_data/classified/')
        


import re
class ImagesM(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = None
        self.index = None
        self.images = None
        self.current_image = None

    def load_images(self, path):
        self.path = path
        self.images = [x for x in os.listdir(f'{path}') if re.search('\.gif$|\.jpg$|\.jpeg$|\.png$',x )]
        self.index = 0
        self.current_image = f'{self.path}{self.images[self.index]}'

    def next(self):
        self.index = self.index + 1 if self.index < len(self.images) - 1 else 0
        self.current_image = f'{self.path}{self.images[self.index]}'
        return self.current_image
    
    def prev(self):
        self.index = self.index - 1 if self.index > 0 else len(self.images) - 1
        self.current_image = f'{self.path}{self.images[self.index]}'
        return self.current_image