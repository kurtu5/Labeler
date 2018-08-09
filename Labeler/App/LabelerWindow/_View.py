# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from PySide2.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QGridLayout, QStackedLayout, QGraphicsWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QIcon, QImageReader, QPixmap, QFont, QColor
from PySide2.QtCore import QFile, QSize, QEvent, QObject, Signal, QItemSelectionModel, QRectF, QSizeF, Qt, Signal
from PySide2.QtWidgets import QLayout, QFormLayout, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QGraphicsGridLayout
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QTransform


#https://github.com/tpgit/MDIImageViewer seems to do everything....
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
import MVPBase

class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_id = None   # Canvas image id
        self.image_orig = None # PIL.Image
        self.debug = False

#         self.controller = controller
        self.label_widgets = {}
        
        self.image_signal = self.ImageSignal()

#        self.font = Font(size=24)
        self.default_scale = 0.2
        self.scale = 1.0;   # Initial Image scale
#        self.scale_xloc = 0
#        self.scale_yloc = 0
        self.max_columns = 4 # Max cols for multimages
        self.cached_thumbs = {}

            # I could write this to add custom signals for custom events
    class KeyEventFilter(QObject):
        signal = Signal(QEvent)
        def __init__(self, parent, stopHere=False, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.parent = parent
            self.stopHere = stopHere
            self.types = []

        def eventFilter(self, obj, event):
#            print("parent", self.parent)
            #http://www.qtcentre.org/threads/24597-PyQt4-QGraphicsView-and-pressed-signal
            if isinstance(obj, QGraphicsScene):
#                print("QGraphicsScene obj detected,",event.type())
                return False
            if  isinstance(obj, QGraphicsView) :
#                print("QGraphicsView obj detected,",event.type())
                return False
#            if (event.type() == QEvent.Type.GraphicsSceneMouseRelease ):
#                print("Mouse release", obj, ',', obj.objectName())
            if (event.type() == QEvent.KeyPress):
#                print("emittttttttt")
                self.signal.emit(event)
            return self.stopHere

#    def image_list_set(self, items):
#        self.image_listbox.delete(0, 'end')
#        for item in items:
#            self.image_listbox.insert('end', item)

#    def scroll(self, amount):
#        self.canvas.yview_scroll(amount, "units")

#    def image_load(self, file):
##        self.scale = self.default_scale
#        self.image_orig = Image.open(file)

#    def image_update(self, scale=1, scale_xloc=0, scale_yloc=0):
       # old canvas redrawer


#    def set_label_widget(self, key, has_feature):
#        if has_feature == 1:
#            self.label_widgets[key].config(foreground="green")
#        if has_feature == 0:
#            self.label_widgets[key].config(foreground="red")
#        if has_feature == -1:
#            self.label_widgets[key].config(foreground="grey")

#    def create_label_widgets(self):
##  TODO       shortcuts_labels = controller.models[LabelerModel].shortcuts_labels
#        shortcuts_labels = {"q": "feat1", "w": "feat2", "e": "feat3", "r": "other"}
#
#        for k,v in shortcuts_labels.items():
#            tmp = self.tk.Frame(self.left_frame)
##            tmp.pack(side='left', padx=40, expand=True )
#            tmp.grid(sticky='w', padx=40)#, expand=True )
#
#            self.tk.Label(tmp,text='Key: '+k).grid()
#
#            self.label_widgets[k] = self.tk.Label(tmp, text=v)
#            self.label_widgets[k].config(foreground="grey", font=self.font)
##            self.label_widgets[k].pack()
#            self.label_widgets[k].grid()

    def image_scale(self, factor):
        self.scale = self.scale * factror
        gv.setTransform(QTransform(self.scale,0,0,self.scale,0,0))

    # This works
    def image_loade(self, images):
        print("called")
        l = QVBoxLayout()
        self.page.display.setLayout(l)
        
        sc = QGraphicsScene()
        sc2 = QGraphicsScene()

        gv = QGraphicsView()
        gv2 = QGraphicsView()
        gv.setScene(sc)
        gv2.setScene(sc2)
        
        l.addWidget(QLabel("START"))
        l.addWidget(gv)
        l.addWidget(gv2)
        l.addWidget(QLabel("END"))
        
        im1=r"C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/290836_11big.jpg"
        im2=r"C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/368659_12big.jpg"
        image_reader = QImageReader()
        image_reader.setDecideFormatFromContent(True)
        image_reader.setFileName(im1)
        image1 = image_reader.read()
        image_reader.setFileName(im2)
        image2 = image_reader.read()
        pixmap1 = QPixmap(image1)
        pixmap1 = pixmap1.scaledToWidth(100)
        pixmap2 = QPixmap(image2)
        pixmap2 = pixmap2.scaledToWidth(100)
    

        sc.addPixmap(pixmap1)
        sc2.addPixmap(pixmap2)
        
    class ImageSignal(QObject):
        deselected = Signal(int)
        def myemit(self, index):
            self.deselected.emit(index)
            
    def image_load(self, images):
        # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        def clearLayout(layout):
          while layout.count():
            child = layout.takeAt(0)
            if child.widget():
              child.widget().deleteLater()


        print("     inside image_load")
        im1=r"C:/Users/kurt/Documents/fast.ai/fastai/courses/dl1/test_data/classified/290836_11big.jpg"
        image_reader = QImageReader()
        image_reader.setDecideFormatFromContent(True)
        image_reader.setFileName(im1)
        image1 = image_reader.read()


        self.pixmap = None
        num = len(images)
    
        width=self.page.display.width()
        maxcol = self.max_columns
        if num != 0 and num < maxcol:
            maxcol = num
        colwidth = width/maxcol
        col = 0
        row = 0
        
        # Prescan to get max height
        maxHeight = 0
        maxWidth = 1
        for index, image in images.items():

            image_reader = QImageReader()
            image_reader.setDecideFormatFromContent(True)
            image_reader.setFileName(image)
#            image_reader.setScaledSize(QSize(100,100))
            size = image_reader.size()
            height = size.height()
            width = size.width()
            if height > maxHeight:
                maxHeight = height
                maxWidth = width
        rowheight = maxHeight / ( maxWidth / colwidth )
        
        if num <= 1:
            QWidget().setLayout(self.page.display.layout())
            self.display_layout = QGridLayout()
            self.graphicsview = QGraphicsView()
            self.display_layout.addWidget(self.graphicsview)
            self.display_multiple_layout = QGraphicsGridLayout()

            
            self.page.display.setLayout(self.display_layout)
        else:
            QWidget().setLayout(self.page.display.layout())
            self.display_layout = QVBoxLayout()
            self.display_multiple_layout = QGraphicsGridLayout()
            
            self.graphicsview = QGraphicsView()
            self.scene=QGraphicsScene()
            self.graphicsview.setScene(self.scene)
            
            self.panel = QGraphicsWidget()
            self.scene.addItem(self.panel)
            
            self.display_layout.addWidget(self.graphicsview)

            self.panel.setLayout(self.display_multiple_layout)
#            self.graphicsview.setLayout(self.display_multiple_layout)
            

            
            clearLayout(self.display_multiple_layout)
            self.page.display.setLayout(self.display_layout)
#            self.display_multiple_layout.setHorizontalSpacing(400) # forced big

#            self.display_multiple_layout.setSizeConstraint(QLayout.SetMaximumSize)
#            size = QSize(400,400)
#            self.display_multiple_layout.setSizeHint(size)
#            print("mult=",self.display_multiple_layout.sizeHint())
            
        for index, image in images.items():

            if col >= maxcol:
                col = 0
                row += 1

            image_reader = QImageReader()
            image_reader.setDecideFormatFromContent(True)
            image_reader.setFileName(image)
#            image_reader.setScaledSize(QSize(100,100))
            img = image_reader.read()
            
            scene = QGraphicsScene()
            gv = QGraphicsView()
            gv.setScene(scene)

            pixmap = QPixmap(img)
            if num != 1:
#                print("multiimage")
                pixmap = pixmap.scaledToWidth(colwidth - 20)
                item = scene.addPixmap(pixmap)
#                item.setOffset(col * colwidth, row * rowheight)
                ql = QLabel("TEST")
                ql.resize(500,500)
                s = 50
                import ntpath
                filename=ntpath.basename(image)
#                if index not in self.cached_thumbs.keys():
#                    print("Creating cache for index=",index)
                rec = self.RectangleWidget(pixmap, filename, index)
                rec.deselected.connect(self.image_signal.myemit)
#                    self.cached_thumbs[index] = rec

#                print("Size = ", rec.size())
                self.display_multiple_layout.addItem(rec, row, col)
#                for i in [0,1,2,3]:
#                    w = self.display_multiple_layout.columnMinimumWidth(i)
#                    print(f"col {i} is w={w}")

            else:
                self.display_layout.addWidget(gv, row, col)
                scene.addPixmap(pixmap)

            col += 1
 
            
    class RectangleWidget(QGraphicsWidget):
        deselected = Signal(int)
        def __init__(self, pixmap, filename, index, parent=None):
            super().__init__(parent)
#            self.rect = rect
            self.pixmap = pixmap
            self.filename = filename
            self.index = index
            self.setMinimumSize(QSizeF(self.pixmap.size()))
            self.setMaximumSize(QSizeF(self.pixmap.size()))
            defaultFont = QFont("default/font-family")
            self.label_font = defaultFont

            
        def mousePressEvent(self, event):
            print("Remove index=", self.index)
            self.deselected.emit(self.index)

            return
            print("Hover", event.type())
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ShiftModifier:
                print('Shift+Click')
            elif modifiers ==  Qt.ControlModifier:
                print('Control+Click')
            elif modifiers == ( Qt.ControlModifier |
                                Qt.ShiftModifier):
                print('Control+Shift+Click')
            elif modifiers == ( Qt.AltModifier):
                print('Alt')
            else:
                print('Click')
            
                

        def paint(self, painter, *args, **kwargs):
#            print('Paint Called')
#            painter.drawRect(self.rect)
            painter.drawPixmap(0, 0, self.pixmap)
#            self.label_font.setColor(QColor("red"))
            width = self.pixmap.size().width()
            # Any width below key is size
            font_step_size = {40:2, 60:4, 80:6, 100:8, 140:10, 160:12, 180:14, 200:16}
            for w,s in font_step_size.items():
                pixel_size = s
                if width < w:
                    break
#            print("width,pixelsize", width,pixel_size)
            # 212 = 20  31=6
            self.label_font.setPixelSize(pixel_size)
            painter.setFont(self.label_font)
#            painter.setPen(QColor("red"))
            painter.drawText(1,self.pixmap.size().height()+pixel_size,self.filename)
            size = QSizeF(self.pixmap.size())
            textsize = QSizeF(0,pixel_size)
            newsize = size + textsize
            self.setMaximumSize(newsize)
            self.setMinimumSize(newsize)

#        self.gv.show()
#        item=QGraphicsItem()
#        gv.setInteractive(False)
#        print("GV isinteractive =", gv.isInteractive())



    def image_list_setSelected(self, index, select=True):
#        print("start image_list_setSelected")
        if select == True:
            self.page.listWidget.setCurrentRow(index, QItemSelectionModel.Select)
        else:
            self.page.listWidget.setCurrentRow(index, QItemSelectionModel.Toggle)

#        print("     fin image_list_setSelected")



    def image_list_update(self, images):
        """ Put all the images in the QListWidget """
        size = 60
#        self.page.listWidget.setIconSize(QSize(size,size))

        for image in images:

            item = QListWidgetItem()

            import ntpath
            filename=ntpath.basename(image)
#            item.setText(f'{filename}')

            widget = QWidget()
            widgetText = QLabel(f'{filename}')
            widgetLabels = QLabel("QWER")
#            l = QLabel("XXX")
#            l.setParent(item)


#            font=QFont("Times",10, QFont.Bold)
#            item.setFont(font)
#            item.setSizeHint(size)


            image_reader = QImageReader()
            image_reader.setDecideFormatFromContent(True)
            image_reader.setFileName(image)
            image_reader.setScaledSize(QSize(size,size))
            img = image_reader.read()
            pixmap= QPixmap(img)
#            pixmap.scaled(QSize(size,size))

            icon=QIcon(pixmap)
            widgetIcon = QLabel()
            widgetIcon.setPixmap(pixmap)
            widgetLayout = QHBoxLayout()


            widgetLayout.addWidget(widgetLabels)
            widgetLayout.addWidget(widgetIcon)
            widgetLayout.addWidget(widgetText)
            widgetLayout.addStretch()

            widget.setLayout(widgetLayout)
#            pixmap=icon.pixmap(100,100)
#            item.setIcon(icon)
#            item.setSizeHint(QSize(size,size))
            item.setSizeHint(widget.sizeHint())


            self.page.listWidget.addItem(item)
            self.page.listWidget.setItemWidget(item, widget)

    def start(self):
            # Since I have default implemetations for showable pages, do this in base?
            path = os.path.dirname(os.path.realpath(__file__)) + "\\"
            file = QFile(path + "labeler.ui")
            file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.page = loader.load(file)
#            gv = self.page.graphicsView
            

            
#            self.display_layout = QGridLayout()
#            self.display_multiple_layout = QGridLayout()
#
#            self.graphicsview = QGraphicsView()
#            self.scene = QGraphicsScene()
#            self.display_layout.addWidget(self.graphicsview)
#            self.page.display.setLayout(self.display_layout)
            

            
            self.page_index = self.parent.stacked_widget.addWidget(self.page)
            self.page.columns_choice.setRange(1,10)
            self.page.columns_choice.setValue(4)
            
#            size=QSize()
#            size.boundedTo(QSize(300,300))
#            size.expandedTo(QSize(300,300))
#            self.page.listWidget.setIconSize(size)
            self.page.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

            # Global key press eventFilter.signal emits
            self.keyEvent = self.KeyEventFilter(self.parent.parent)
            self.parent.parent.installEventFilter(self.keyEvent)
