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

from GenericWindow._Model import Model
from GenericWindow._View import View
from GenericWindow._Presenter import Presenter
from GenericWindow._Interactor import Interactor
from GenericWindow._Observer import Observer
