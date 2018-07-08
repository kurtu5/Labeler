# -*- coding: utf-8 -*-

class StatusBar(tk.Label):
    """ Status line to indicate saved status """
    # I dont think this is stricky needed
    def __init__(self, parent):
        tk.Label.__init__(self, parent)
        self.config(bd=2, relief='groove', anchor='w')
        self.grid(sticky='we', padx=2, pady=2)
    def update(self, text):
        self.config(text=text)
    