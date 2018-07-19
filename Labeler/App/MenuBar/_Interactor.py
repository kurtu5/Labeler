# -*- coding: utf-8 -*-

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

# TODO: when binds are registered, have some way to allow the presetner
# to disable them
class Interactor(MVPBase.BaseInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # called by mvpbase_presenter.start()
    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)
        # now view and presenter are coupled
        self.callback_register_all()

    def callback_register_all(self):
        p = self.presenter
        v = self.view
        fm=v.filemenu.add_command
        fm(label='Exit', command=p.on_app_exit)

        vm=v.viewmenu.add_command
        vm(label='Test', command=lambda: p.on_window_show('test'))
        vm(label='Labeler', command=lambda: p.on_window_show('labeler'))
        vm(label='Options', command=lambda: p.on_window_show('options'))

