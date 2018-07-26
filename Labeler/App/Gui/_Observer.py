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

class Observer(MVPBase.BaseObserver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        super().start(*args, **kwargs)

    def event_all_register(self):
        """ set callbacks for events generated by model """
        presenter = self.presenter

        def close(enable):
            if enable == True:
                presenter.on_app_exit()

        self.event_add(('app_exit', close))
        self.event_add(('status_text', presenter.on_status_text))
        self.event_add(('app_open', presenter.on_app_open))

        # TODO If I want the gui to change if a window raised, do this
#        foo = self.callback_add('window_model_current', presenter.on_window_show)