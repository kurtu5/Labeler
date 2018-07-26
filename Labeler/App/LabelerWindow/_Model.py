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
        testdata = os.path.normpath(
        "C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/")
        print("other models = ", self.other_models)
        self.sib('images').load_images(testdata)
