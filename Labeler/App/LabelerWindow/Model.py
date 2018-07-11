# -*- coding: utf-8 -*-
import MVPBase

class Model(MVPBase.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def start(self):
#         print('labeler i should tell gui that im showable'
        self.other_models['images'].load_images('data/unclassified/')
        