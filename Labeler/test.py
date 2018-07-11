# Bullshit to allow "python blah/blah/file.py"
import sys
sys.path = [''] + sys.path

from Labeler.App import App

# Do some tests
