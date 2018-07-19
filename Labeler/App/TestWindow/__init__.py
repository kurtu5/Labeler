#print(f'import LabelerWindow __init__ __name__={__name__}')

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from TestWindow._Model import Model
from TestWindow._View import View
from TestWindow._Presenter import Presenter
from TestWindow._Interactor import Interactor
from TestWindow._Observer import Observer