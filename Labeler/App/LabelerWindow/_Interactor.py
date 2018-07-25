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
        """ set callbacks for events generated by view """
        p = self.presenter
        v = self.view
        add = self.event_add

        # Canvas scroll and zoom clicks
        add((v.canvas, '<MouseWheel>', p.on_mouse_wheel), 'scroll')
        # Left to zoom in, middle to reset and right to zoom out
        mult = 1.5
        add((v.canvas, '<Button 1>', lambda e: p.on_scale(mult, e)), 'zoom')
        add((v.canvas, '<Button 2>', lambda e: p.on_scale(1.0, e)), 'zoom')
        add((v.canvas, '<Button 3>',lambda e: p.on_scale(1/mult, e)), 'zoom2')

        from tkCustom._Debug import D
        def enter_canvas(e):
            D.ebug('enter canvas')
            v.canvas.focus_set()
        def exit_canvas(e):
            D.ebug('exit canvas')
            v.main.focus_set()

        add((v.root.master, '<Enter>', enter_canvas), 'canvas_focus')
        add((v.root.master, '<Leave>', exit_canvas), 'canvas_focus')

        add((v.canvas, '<Key>', p.on_keyevent, True),'shortcuts')
