# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from App import App

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    app = App()
    app.run()