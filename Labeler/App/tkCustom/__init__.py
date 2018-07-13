print(f'import Gui __init__ __name__={__name__}')

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from _Bind import Bind
from _AutoScrollBar import AutoScrollbar
from _AutoSizeGrip import AutoSizegrip
from _StatusBar import StatusBar
from _Debug import D

#__all__ = ['Model', 'View', 'Presenter']