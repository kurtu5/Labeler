#print(f'import MenuBar __init__ __name__={__name__}')

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from MenuBar._Model import Model
from MenuBar._View import View
from MenuBar._Presenter import Presenter

#__all__ = ['Model', 'View', 'Presenter']