from time import sleep
import tkinter as tk

class D():
    """ Just a help class to put debug text int the tkinter window """
    def __init__(self, root, height=2):
        D.root = root
        D.height = height
#         D.wd = tk.Label(D.root, text="Debugging sstuff here")
        D.frame=tk.Frame(D.root)
        D.frame.grid_columnconfigure(0, weight=1)
        D.frame.grid_columnconfigure(1, weight=0)
    
        D.scrollbar = tk.Scrollbar(D.frame, orient='vertical')
        D.listbox = tk.Listbox(D.frame, height=self.height, yscrollcommand=D.scrollbar.set)
        
        D.listbox.grid(column=0, row=0, sticky='nsew')
        D.scrollbar.grid(column=1, row=0, sticky='ns')
        
        D.scrollbar.config(command=D.listbox.yview)
        
        D.frame.grid(column=0, row=2, sticky='nsew')
       
    @staticmethod
    def ebug(txt):
#        D.listbox.config(bg='lightgrey')
        D.listbox.insert(0, txt)
        size = D.listbox.size()
        for index in range(size):
            D.listbox.itemconfig(index, {'fg': 'black'})
        D.listbox.itemconfig(0, {'fg': 'red'})

        def debug_listbox_flash_off():
            D.listbox.itemconfig(0, {'fg': '#500000'})
        D.listbox.after(600, debug_listbox_flash_off )

