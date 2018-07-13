print(f'import MVPBase __init__ __name__={__name__}')

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from _BaseModel import ModelBase
from _BaseView import ViewBase
from _BasePresenter import PresenterBase
from _BaseCommand import CommandBase
from _BaseInteractor import InteractorBase
from _BaseObservable import ObservableBase
#
#__all__ = [
#        'Model',
#        'View',
#        'Presenter',     
#        'Command',
#        'Interactor',
#        'Observable'
#        ]