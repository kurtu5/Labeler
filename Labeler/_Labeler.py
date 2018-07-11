import sys
from Labeler.App import App

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

#    print(f"dir of app { dir(App)}")
    app = App()
    app.run()