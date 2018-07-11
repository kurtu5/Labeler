# Bullshit to allow "python blah/blah/file.py"
import sys
sys.path = [''] + sys.path


import Labeler

# Do some tests
#Labeler.main()