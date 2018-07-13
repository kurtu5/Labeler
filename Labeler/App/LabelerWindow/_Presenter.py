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
Observable = MVPBase.Observable

class Presenter(MVPBase.PresenterBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = None
        self.default_scale = 1.0
        self.image_id = False
        self.image_orig = None
        self.start()
        
    def start(self):
        self.setbindings()
         # Let guiM know im showable
        self.model.other_models['gui'].window_showable_add('labeler', self.view.main)
        # Have imagesM load images
            ### done alread in labelerM start 
        # Load and Show first imagesM has loaded
        self.image_load(self.model.other_models['images'].current_image)
        self.image_show()
    
    def bindcanvas(self, seq, func):
        self.view.bind.register(self.view.canvas, seq, func)

    def setbindings(self):

        self.bindcanvas('<MouseWheel>', self.OnMouseWheel)
        self.bindcanvas('<space>', lambda e: self.OnScroll(2))
        self.bindcanvas('<Down>', lambda e: self.OnScroll(2))
        self.bindcanvas('<Up>', lambda e: self.OnScroll(-2))
        # Left to zoom in, middle to reset and right to zoom out
        self.bindcanvas('<Button 1>', lambda e: self.OnScale(1.3, e))
        self.bindcanvas('<Button 2>', lambda e: self.OnScale(1, e))
        self.bindcanvas('<Button 3>', lambda e: self.OnScale(0.7, e))
        self.bindcanvas('<Button 4>', lambda e: D.ebug('button 4 canvas'))
        self.bindcanvas('<Enter>', lambda e: D.ebug('enter canvas'))
        self.bindcanvas('<Leave>', lambda e: D.ebug('leave canvas'))
        
        
#         bind1 = self.view.bind.register(self.view.canvas, '<Key>', self.keypress2)

        self.view.canvas.focus_set()
        self.view.bind.activate_all(active=True)
        pass



#         self.bindcanvas('<Enter>', lambda e: self.leave('enter canvas'))
        
    def keypress2(self, event):
        D.ebug('key pressed')
        
    def OnScale(self, scale, event):
#         print("scale", self.scale, "eventxy", event.x, event.y)
        if scale == 1:
            self.scale = 1.0
        else:
            self.scale *= scale;
            self.scale_xloc = event.x
            self.scale_yloc = event.y
        self.image_show()
        
    def OnScroll(self, amount):
        self.view.canvas.yview_scroll(amount, "units")

    def OnMouseWheel(self, event):
        print(event)
#         print("mouse scroll","scroll",event.delta,"units")
        amount = 0
        # Deal with linux and windows events
        if event.num == 5 or event.delta == -120:
            amount += 1
        elif event.num == 4 or event.delta == 120:
            amount -= 1
#         print("scroll by ", amount)
        self.OnScroll(amount)      
        
    def image_load(self, fname):
        self.scale = self.default_scale
        self.image_orig = Image.open(fname)  
      
    def image_show(self):
        #delete and redraw if scaled
        if self.image_id:
            self.view.canvas.delete(self.image_id)
        
        # Conditionaly scale
        if self.scale != 1.0:
#             print("scaling image")
            # Do stuff to center zoomed in middle
            cw = self.view.canvas.winfo_reqwidth()  
            ch = self.view.canvas.winfo_reqheight()
            x = self.scale_xloc
            y = self.scale_yloc
            cx = self.view.canvas.canvasx(x)
            cy = self.view.canvas.canvasy(y)
            hcw = self.view.canvas.winfo_width() / 2
            hch = self.view.canvas.winfo_height() / 2
            px = (cx - hcw) / cw
            py = (cy - hch) / ch
            #D.ebug(f'cw,ch = {cw},{ch},  x,y = {x}, {y}, cx,cy = {cx},{cy}, hcw,hch={hcw},{hch},  px,py = {px*100:.0f},{py*100:.0f} ')
       
            iw, ih = self.image_orig.size
            size = int(iw * self.scale), int(ih * self.scale)
            img = ImageTk.PhotoImage(self.image_orig.resize(size))

            self.image_id = self.view.canvas.create_image(0, 0, anchor='nw', image=img)
        else:
#             print("not scaling image")
            px = 0
            py = 0
            img = ImageTk.PhotoImage(self.image_orig)
            self.image_id = self.view.canvas.create_image(0,0, anchor='nw', image=img)

        self.view.canvas.image = img
        self.view.canvas.config(scrollregion=(0,0, img.width(), img.height()))
        self.view.canvas.config(height=img.height(), width=img.width())
      
        # Update status string
        fname = self.image_orig.filename
        index = 'idx'
        self.model.other_models['gui'].statustext.set(f'index: ?  image: {self.image_orig.filename}  scale: {self.scale}')
        # Reset scrollbars
        self.view.canvas.xview('moveto', px)
        self.view.canvas.yview('moveto', py)
        
        
