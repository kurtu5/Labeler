#print(f'import tkCustom __init__ __name__={__name__}')

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from tkCustom._Bind import Bind
from tkCustom._AutoScrollBar import AutoScrollbar
from tkCustom._AutoSizeGrip import AutoSizegrip
from tkCustom._StatusBar import StatusBar
from tkCustom._Debug import D

#__all__ = ['Model', 'View', 'Presenter']