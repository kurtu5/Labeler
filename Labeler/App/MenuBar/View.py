# -*- coding: utf-8 -*-

from Labeler.App.MVPBase.Presenter import Presenter
class View(App.MVPBase.View):
    def __init__(self, *args, **kwargs):
#         print('menubarV init')
        super().__init__(*args, **kwargs)
        self.menu = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        
        self.viewmenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='View', menu=self.viewmenu)
        
        
    def start(self):
#             print('============menu started')
            super().start()
            self.root.config(menu=self.menu)
            self.filemenu.add_command(label='Exit', command=self.presenter.closeapp)
            self.viewmenu.add_command(label='Test', command=lambda: self.presenter.show_window('test'))
            self.viewmenu.add_command(label='Labeler', command=lambda: self.presenter.show_window('labeler'))
