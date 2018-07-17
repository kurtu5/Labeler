#print(f'import Images __init__ __name__={__name__}')

# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from Images._Model import Model
#from Images._View import View
#from Images._Presenter import Presenter
#from Images._Interactor import Interactor
#from Images._Observer import Observer