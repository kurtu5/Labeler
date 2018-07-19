# Bullshit to allow "python blah/blah/file.py"
# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = ''
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import Labeler
Labeler.main()

# Do some tests
#Labeler.main()