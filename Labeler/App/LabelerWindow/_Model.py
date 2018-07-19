# -*- coding: utf-8 -*-

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

testdata = os.path.normpath(
        "C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/")

class Model(MVPBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.window_enabled = False

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
#        self.window_enabled = self.observer.observe_as('window_enable', False)

        #         print('labeler i should tell gui that im showable'
        self.others['images'].load_images(testdata)
