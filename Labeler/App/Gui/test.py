# Bullshit to allow "python blah/blah/file.py"
import sys
sys.path = [''] + sys.path

#from ..Base import Base


#from Labeler.App.MVPBase.Model import Model
import Labeler.App.MVPBase as B
#
#class Test(Model):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#
#fakemodel = 'fake instance of Model'
#test = Test('modelname', {'name1': fakemodel})