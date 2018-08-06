# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from tkinter.font import Font
from PIL import ImageTk, Image

import MVPBase

class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_id = None   # Canvas image id
        self.image_orig = None # PIL.Image
        self.debug = False

#         self.controller = controller
        self.label_widgets = {}

        self.font = Font(size=24)
        self.default_scale = 0.2
#        self.scale = 1.0;   # Initial Image scale
#        self.scale_xloc = 0
#        self.scale_yloc = 0

    def image_list_set(self, items):
        self.image_listbox.delete(0, 'end')
        for item in items:
            self.image_listbox.insert('end', item)

    def scroll(self, amount):
        self.canvas.yview_scroll(amount, "units")

    def image_load(self, file):
#        self.scale = self.default_scale
        self.image_orig = Image.open(file)

    def image_update(self, scale=1, scale_xloc=0, scale_yloc=0):
        #delete and redraw if scaled
        if self.image_id:
            self.canvas.delete(self.image_id)

        # Conditionaly scale
        if scale != 1.0:
            # Do stuff to center zoomed in middle
            cw = self.canvas.winfo_reqwidth()
            ch = self.canvas.winfo_reqheight()
            x = scale_xloc
            y = scale_yloc
            cx = self.canvas.canvasx(x)
            cy = self.canvas.canvasy(y)
            hcw = self.canvas.winfo_width() / 2
            hch = self.canvas.winfo_height() / 2
            px = (cx - hcw) / cw
            py = (cy - hch) / ch
            #D.ebug(f'cw,ch = {cw},{ch},  x,y = {x}, {y}, cx,cy = {cx},{cy}, hcw,hch={hcw},{hch},  px,py = {px*100:.0f},{py*100:.0f} ')

            iw, ih = self.image_orig.size
            size = int(iw * scale), int(ih * scale)
            img = ImageTk.PhotoImage(self.image_orig.resize(size))

            self.image_id = self.canvas.create_image(0, 0, anchor='nw', image=img)
        else:
            px = 0
            py = 0
            img = ImageTk.PhotoImage(self.image_orig)
            self.image_id = self.canvas.create_image(0,0, anchor='nw', image=img)

        self.canvas.image = img
        self.canvas.config(scrollregion=(0,0, img.width(), img.height()))
        self.canvas.config(height=img.height(), width=img.width())
        # Reset scrollbars
        self.canvas.xview('moveto', px)
        self.canvas.yview('moveto', py)

    def debugFrame(self, parent, text, on=True):
        if self.debug == True:
            return self.tk.LabelFrame(parent, text=text)
        elif self.debug == False:
            return self.tk.Frame(parent)

    def set_label_widget(self, key, has_feature):
        if has_feature == 1:
            self.label_widgets[key].config(foreground="green")
        if has_feature == 0:
            self.label_widgets[key].config(foreground="red")
        if has_feature == -1:
            self.label_widgets[key].config(foreground="grey")

    def create_label_widgets(self):
#  TODO       shortcuts_labels = controller.models[LabelerModel].shortcuts_labels
        shortcuts_labels = {"q": "feat1", "w": "feat2", "e": "feat3", "r": "other"}

        for k,v in shortcuts_labels.items():
            tmp = self.tk.Frame(self.left_frame)
#            tmp.pack(side='left', padx=40, expand=True )
            tmp.grid(sticky='w', padx=40)#, expand=True )

            self.tk.Label(tmp,text='Key: '+k).grid()

            self.label_widgets[k] = self.tk.Label(tmp, text=v)
            self.label_widgets[k].config(foreground="grey", font=self.font)
#            self.label_widgets[k].pack()
            self.label_widgets[k].grid()


    def start(self):

        self.main = self.debugFrame(self.root, text="labler main")
        self.main.grid(column=0, row=0, sticky='nsew')

#         self.main.grid(column=0, row=1, sticky='nsew')  # 1 col, 2 rows; top bottom
        self.main.grid_columnconfigure(1, weight=1)  # widen middle on resize
        self.main.grid_rowconfigure(0, weight=1)     # heighten bottom on resize

        # Left frame
        self.left_frame = self.debugFrame(self.main, text="left frame")
        self.left_frame.grid(column=0, row=0, sticky='ns')  # fill space
#        self.left_frame.grid_columnconfigure(0, weight=1) # allow child to widen
#        self.left_frame.grid_rowconfigure(0, weight=1) # allow child to heighten

        # Middle
        self.middle_frame = self.debugFrame(self.main, text="middle frame")
        self.middle_frame.grid(column=1, row=0, sticky='nsew')
        self.middle_frame.grid_columnconfigure(0, weight=1) # allow child to fill xy
        self.middle_frame.grid_rowconfigure(0, weight=1)

       # Right
        self.right_frame = self.debugFrame(self.main, text="right frame")
        self.right_frame.grid(column=2, row=0, sticky='ns')
#        self.right_frame.grid_columnconfigure(0, weight=1)
        self.image_listbox = self.tk.Listbox(self.right_frame)
        self.image_listbox.grid()
        # Bottom
        self.bottom_frame = self.debugFrame(self.main, text="bottom frame")
        self.bottom_frame.grid(column=0, row=1, columnspan=3, sticky='nsew')
        self.bottom_frame.grid_columnconfigure(0, weight=1)
#         parent.grid_propagate=(0)

        self.tk.Label(self.left_frame, text='example left frame content').grid(sticky='ns')
#        self.tk.Label(self.middle_frame, text='example  middle frame content').grid(sticky='nsew')
#        self.tk.Label(self.right_frame, text='example right frame content').grid(sticky='ns')

#        self.tk.Label(self.bottom_frame, text='example bottom frame content').grid(sticky='ew')
#         tk.Label(self.bottom_frame, text='example').grid(sticky='nsew')

        self.canvas_frame = self.debugFrame(self.middle_frame, text='image')
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid()

        self.xscrollbar = self.tkc.AutoScrollbar(self.canvas_frame, orient='horizontal')
        self.xscrollbar.grid(column=0, row=1, sticky='ew')
#         self.xscrollbar.grid_remove()

        self.yscrollbar = self.tkc.AutoScrollbar(self.canvas_frame, orient='vertical')
        self.yscrollbar.grid(column=1, row=0, sticky='ns')


        self.canvas = self.tk.Canvas(self.canvas_frame,
                        xscrollcommand=self.xscrollbar.set,
                        yscrollcommand=self.yscrollbar.set)

        # Binds done in presenter/interacor

        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)

#         self.create_label_widgets()   # TODO let the models
#         controller.mcs[LabelerMC].update_label_widgets()

        self.create_label_widgets()
