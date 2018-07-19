# Bullshit to allow "python blah/blah/file.py"
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

#from ..Base import Base


#from Labeler.App.MVPBase.Model import Model
import MVPBase
#
#class Test(Model):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#
#fakemodel = 'fake instance of Model'
#test = Test('modelname', {'name1': fakemodel})