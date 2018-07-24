# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from MVPBase._BaseModel import BaseModel
from MVPBase._BaseView import BaseView
from MVPBase._BasePresenter import BasePresenter
from MVPBase._BaseInteractor import BaseInteractor
from MVPBase._BaseObserver import BaseObserver
#
#__all__ = [
#        'Model',
#        'View',
#        'Presenter',
#        'Command',
#        'Interactor',
#        'Observable'
#        ]