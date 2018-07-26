# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

import MVPBase

class Interactor(MVPBase.BaseInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

    def event_all_register(self):
        # These events are always bound and dont use interactor
        p = self.presenter
        v = self.view
        fm=v.filemenu.add_command
        fm(label='Open', command=p.on_app_open)
        fm(label='Exit', command=p.on_app_exit)

        vm=v.viewmenu.add_command
        vm(label='Test', command=lambda: p.on_window_enable('test'))
        vm(label='Labeler', command=lambda: p.on_window_enable('labeler'))
        vm(label='Options', command=lambda: p.on_window_enable('options'))