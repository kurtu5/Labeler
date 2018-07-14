#print(f'import MVPBase __init__ __name__={__name__}')

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from MVPBase._BaseModel import ModelBase
from MVPBase._BaseView import ViewBase
from MVPBase._BasePresenter import PresenterBase
from MVPBase._Command import Command
from MVPBase._Interactor import Interactor
from MVPBase._Observable import Observable
#
#__all__ = [
#        'Model',
#        'View',
#        'Presenter',     
#        'Command',
#        'Interactor',
#        'Observable'
#        ]