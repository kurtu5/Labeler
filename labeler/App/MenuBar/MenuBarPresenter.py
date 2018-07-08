# -*- coding: utf-8 -*-

class MenuBarP(Presenter):
    def __init__(self, *args, **kwargs):
#         print('menubar P init')
        super().__init__(*args, **kwargs)
        self.start()
        
    def start(self):
        super().start()
    
    def closeapp(self):
        # Just call the gui model as no menu states need to change
        self.model.other_models['gui'].closeapp()
    
    def show_window(self, window_name):
        self.model.other_models['gui'].window_current(window_name)
#         print('call raise in guimodel to raise the class window')