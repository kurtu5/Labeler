# Bullshit to allow "python blah/blah/file.py"
import sys
sys.path = [''] + sys.path

# See if I can import derived classes
import Labeler.App.Gui as Gui

# Do some tests
