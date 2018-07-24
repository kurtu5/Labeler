# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.append(path)

from App import App
from _Labeler import main


    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
#    app = App()
#    app.run()
