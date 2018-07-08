
import sys
from App.App import App

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

#    print(f"dir of app { dir(App)}")
   
    _application = App()
    _application.run()

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
#    app = App()
#    app.run()
#    
if __name__ == "__main__":
    main()