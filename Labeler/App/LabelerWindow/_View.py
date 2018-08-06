# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)

from PySide2.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QGridLayout
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QIcon, QImageReader, QPixmap
from PySide2.QtCore import QFile, QSize, QEvent, QObject, Signal, QItemSelectionModel
from PySide2.QtWidgets import QFormLayout, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView
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

#        self.font = Font(size=24)
        self.default_scale = 0.2
        self.scale = 1.0;   # Initial Image scale
#        self.scale_xloc = 0
#        self.scale_yloc = 0

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


    def image_load(self, images):

        gv = self.page.graphicsView

        gv.setDragMode(QGraphicsView.ScrollHandDrag)
        gv.setDragMode(QGraphicsView.RubberBandDrag)
#        gv.shear(0.1,0.1)
#        gv.rotate(90)
        scene=QGraphicsScene()
        gv.setScene(scene)
        grid = QGridLayout()
        gv.setLayout(grid)

        num = len(images)
        width=gv.width()
        pixmap = None
        rowWidth = 4
        xCoord = 0
        col = 0
        for image in images:

            image_reader = QImageReader()
            image_reader.setDecideFormatFromContent(True)
            image_reader.setFileName(image)
#            image_reader.setScaledSize(QSize(100,100))
            img = image_reader.read()
            pixmap = QPixmap(img)
            item = scene.addPixmap(pixmap)

            if num != 0:
                pixmap = pixmap.scaledToWidth(width)
                item.setOffset(xCoord, xCoord)

            col += 1
            xCoord += 100


#        item=QGraphicsItem()
#        gv.setInteractive(False)
#        print("GV isinteractive =", gv.isInteractive())



    def image_list_setSelected(self, index):
        self.page.listWidget.setCurrentRow(index, QItemSelectionModel.Select)

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
            gv = self.page.graphicsView

            self.page_index = self.parent.stacked_widget.addWidget(self.page)
#            size=QSize()
#            size.boundedTo(QSize(300,300))
#            size.expandedTo(QSize(300,300))
#            self.page.listWidget.setIconSize(size)
            self.page.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

            # Global key press eventFilter.signal emits
            self.keyEvent = self.KeyEventFilter(self.parent.parent)
            self.parent.parent.installEventFilter(self.keyEvent)
