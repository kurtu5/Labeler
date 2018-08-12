# Make import work like include(./../pkg)
import os, sys
try:
    file = __file__
except:
    file = sys.argv[0]
suffix = '\\..'
path=os.path.dirname(os.path.abspath(__file__)) + suffix
sys.path.insert(0, path)


from ntpath import basename
from PySide2.QtWidgets import QLabel, QPushButton, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QGridLayout, QStackedLayout, QGraphicsWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QIcon, QImageReader, QPixmap, QFont, QColor
from PySide2.QtCore import QFile, QSize, QEvent, QObject, Signal, QItemSelectionModel, QRectF, QSizeF, Qt, Signal
from PySide2.QtWidgets import QLayout, QFormLayout, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QGraphicsGridLayout
from PySide2.QtWidgets import QApplication, QStackedWidget
from PySide2.QtGui import QTransform, QWindow, QPalette, QColor, QPainter


import time

class FeatureStyle:
    has = None
    hasnt = None
    unknown = None
    unsure = None
    _init_already = False
    
    def __init__(self):
        if self._init_already == True:
            return
        self._init_already = True
        self.has = QColor(Qt.green)
        self.hasnt = QColor(Qt.red)
        self.unknown = QColor(Qt.gray)
        self.unsure = QColor(Qt.blue)
        self.conflicting = QColor(Qt.black)
    
class LabelerWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_layout = QGridLayout()
        self.shortcuts = {} # shortcut := {'status': '', 'widget': widget}
        
        self.pal = QPalette()
        self.feature = FeatureStyle()

        self.start()
        
    def start(self):
        self.setLayout(self.grid_layout)
       
    def set_shortcuts_labels(self, shortcuts_labels):
        self.shortcuts = {}
        self.grid_layout.addWidget(QLabel("Key Combos"), 0,0,1,0)
        self.grid_layout.addWidget(QLabel("None"), 1,0,)
        self.grid_layout.addWidget(QLabel("Yes"), 1,1,)
        self.grid_layout.addWidget(QLabel("Shift"), 2,0,)
        self.grid_layout.addWidget(QLabel("No"), 2,1,)
        self.grid_layout.addWidget(QLabel("Control"), 3,0,)
        self.grid_layout.addWidget(QLabel("Not set"), 3,1,)
        self.grid_layout.addWidget(QLabel("Control+Shift"), 4,0,)
        self.grid_layout.addWidget(QLabel("Unsure"), 4,1,)
        row = 4
        col = 0
        for shortcut, label in shortcuts_labels.items():
            row += 1
            shortcut_w = QLabel(f'short={shortcut}')
            label_w = QLabel(f'label={label}')
            self.pal.setColor(QPalette.WindowText, self.feature.unknown)
            shortcut_w.setPalette(self.pal)
            self.shortcuts[shortcut] = {'status': '', 'widget': shortcut_w  }
            self.grid_layout.addWidget(shortcut_w, row, col)
            self.grid_layout.addWidget(label_w, row, col+1)
            
    def set_shortcuts_status(self, shortcut, status):
        self.shortcuts[shortcut]['status'] = status
        bold = QFont()
        bold.setBold(True)
        has_feature = status
        if has_feature == 1:
            self.pal.setColor(QPalette.WindowText, self.feature.has)
        if has_feature == 0:
            self.pal.setColor(QPalette.WindowText, self.feature.unknown)
        if has_feature == -1:
            self.pal.setColor(QPalette.WindowText, self.feature.hasnt)
        if has_feature == 10:
            self.pal.setColor(QPalette.WindowText, self.feature.unsure)
        if has_feature == 'conflicting':
            self.pal.setColor(QPalette.WindowText, self.feature.conflicting)
        self.shortcuts[shortcut]['widget'].setPalette(self.pal)
            
    
class ImageListItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = QWidget()
        self.shortcuts = {}
        self.shortcuts_labels = {}
        self.feature = FeatureStyle()
        self.pal = QPalette()

        self.text_widget = QLabel()

        self.labels_widget = QWidget()
        self.icon_widget = QLabel()
        self.icon_reader = QImageReader()
        
        self.icon_file = None
        self.icon_size = 60
        self.index = None
        self.start()

    def start(self):
        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(self.labels_widget)
        self.shorcutLayout = QVBoxLayout()
        self.labels_widget.setLayout(self.shorcutLayout)
        widgetLayout.addWidget(self.icon_widget)
        widgetLayout.addWidget(self.text_widget)
        widgetLayout.addStretch()
        self.widget.setLayout(widgetLayout)
#            pixmap=icon.pixmap(100,100)
#            item.setIcon(icon)
#            item.setSizeHint(QSize(size,size))
        self.update_size()

    def set_shortcuts_labels(self, shortcuts_labels):
        self.shortcuts = {}

        for shortcut in shortcuts_labels.keys():
            shortcut_w = QLabel(f'{shortcut}')
            self.pal.setColor(QPalette.Text, self.feature.unknown)
            shortcut_w.setPalette(self.pal)

            self.shortcuts[shortcut] = {'status': '', 'widget': shortcut_w  }
            self.shorcutLayout.addWidget(shortcut_w)
        self.update_size()
        
    def set_shortcuts_status(self, shortcut, status):
        self.shortcuts[shortcut]['status'] = status

        has_feature = status
        if has_feature == 1:
            self.pal.setColor(QPalette.Text, self.feature.has)
        if has_feature == 0:
            self.pal.setColor(QPalette.Text, self.feature.unknown)
        if has_feature == -1:
            self.pal.setColor(QPalette.Text, self.feature.hasnt)
        if has_feature == 10:
            self.pal.setColor(QPalette.Text, self.feature.unsure)

        self.shortcuts[shortcut]['widget'].setPalette(self.pal)
        
    def update_size(self):
        self.setSizeHint(self.widget.sizeHint())
        
    def set_index(self, index):
        self.index = index
        
    def set_labels(self, labels):
        self.set_shortcuts_labels(labels)
#        self.update_size()

    def set_text(self, text):
        self.text_widget.setText(text)
        self.update_size()

    def set_icon(self, icon_file):
        self.icon_file = icon_file
        self.update_icon()
        self.update_size()

    def set_icon_size(self, size):
        self.icon_size = size
        self.update_icon()
        self.update_size()

    def update_icon(self):
        self.icon_reader.setDecideFormatFromContent(True)
        self.icon_reader.setFileName(self.icon_file)
        self.icon_reader.setScaledSize(QSize(self.icon_size,self.icon_size))
        image = self.icon_reader.read()
        pixmap = QPixmap(image)
#            pixmap.scaled(QSize(size,size))

#        icon=QIcon(pixmap)
        self.icon_widget.setPixmap(pixmap)


class MultiImageWidget(QGraphicsWidget):
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
#        print("Remove index=", self.index)
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
        self.max_columns = None  # Set when presenter starts # Max cols for multimages
        self.cached_images = {} # Cache read of image from disk

    def start(self):
            # Since I have default implemetations for showable pages, do this in base?
            path = os.path.dirname(os.path.realpath(__file__)) + "\\"
            file = QFile(path + "labeler.ui")
            file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.page = loader.load(file)

            # I could just modify the ui file.... but lets play with this
            self.page.horizontalLayout.removeWidget(self.page.display)
            self.page.leftColumn.removeWidget(self.page.labelerWidget)
            self.page.display.close()
            self.page.labelerWidget.close()
            self.page.display=QStackedWidget()
            self.page.labelerWidget=LabelerWidget()
            self.page.leftColumn.insertWidget(1,self.page.labelerWidget)
            self.page.horizontalLayout.insertWidget(1,self.page.display)
            self.page.horizontalLayout.update()
            
            # Layout for single images
            self.single_image = QWidget()
            self.single_image_layout = QGridLayout()
            self.single_image_view = QGraphicsView()
            self.single_image_scene = QGraphicsScene()
            self.single_image_view.setScene(self.single_image_scene)
            self.single_image_layout.addWidget(self.single_image_view)
            self.single_image.setLayout(self.single_image_layout)

            # Layout for multiple images
            self.multiple_image = QWidget()
            self.multiple_image_view_layout = QVBoxLayout()
            self.multiple_image_layout = QGraphicsGridLayout()
            self.multiple_image_view = QGraphicsView()
            self.multiple_image_scene = QGraphicsScene()
            self.multiple_image_view.setScene(self.multiple_image_scene)
            self.panel = QGraphicsWidget()
            self.multiple_image_scene.addItem(self.panel)
            self.multiple_image_view_layout.addWidget(self.multiple_image_view)
            self.panel.setLayout(self.multiple_image_layout)
            self.multiple_image.setLayout(self.multiple_image_view_layout)

            self.page.display.addWidget(self.single_image)
            self.page.display.addWidget(self.multiple_image)

            self.page_index = self.parent.stacked_widget.addWidget(self.page)
            self.page.columns_choice.setRange(1,10)

#            size=QSize()
#            size.boundedTo(QSize(300,300))
#            size.expandedTo(QSize(300,300))
#            self.page.listWidget.setIconSize(size)
            self.page.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

            # Global key press eventFilter.signal emits
            self.keyEvent = self.KeyEventFilter()
            self.parent.parent.installEventFilter(self.keyEvent)

    def max_columns_choice(self, choice):
        self.max_columns = choice
        self.page.columns_choice.setValue(choice)
        
            # I could write this to add custom signals for custom events
    class KeyEventFilter(QObject):
        KeyPress = Signal(QEvent)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def eventFilter(self, obj, event):
            if event.type() == QEvent.KeyPress and isinstance(obj, QWindow):

#                print(obj, event.text(), "LABLER-------------")
                self.KeyPress.emit(event)
                return False
#            return False
            return QObject.eventFilter(self, obj, event)


#    def scroll(self, amount):
#        self.canvas.yview_scroll(amount, "units")

#    def image_update(self, scale=1, scale_xloc=0, scale_yloc=0):
       # old canvas redrawer



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

#    def image_scale(self, factor):
#        self.scale = self.scale * factror
#        gv.setTransform(QTransform(self.scale,0,0,self.scale,0,0))
#

    class ImageSignal(QObject):
        deselected = Signal(int)
        def myemit(self, index):
            self.deselected.emit(index)
            
    def labeler_widget_load(self):
        pass

    def images_load(self, images):
        """ Take list of images and display in main window """
        num = len(images)
        if num == 0:
            return

        width=self.page.display.width()
        maxcol = self.max_columns
        if num < maxcol:
            maxcol = num
        colwidth = width/maxcol

        # Set proper widget for display of multiple or single images
        if num > 1:
            self.page.display.setCurrentWidget(self.multiple_image)
            # Clear the layout
            while self.multiple_image_layout.count():
                self.multiple_image_layout.removeAt(0)
            # Clear the scene
            for child in self.panel.childItems():
                child.setParent(None)
        else:
            self.page.display.setCurrentWidget(self.single_image)
            self.single_image_scene.clear()
            self.single_image_scene.setSceneRect(self.single_image_scene.itemsBoundingRect())

        # Display images or image
        row = 0
        col = -1
        for index, image_file in images.items():
            col += 1
            if col >= maxcol:
                col = 0
                row += 1

            # Used any cached reads
            if index not in self.cached_images.keys():
                image_reader = QImageReader()
                image_reader.setDecideFormatFromContent(True)
                image_reader.setFileName(image_file)
                self.cached_images[index] = image_reader.read()
            image = self.cached_images[index]

            pixmap = QPixmap(image)
            if num > 1:
                pixmap = pixmap.scaledToWidth(colwidth - 20)
                rec = MultiImageWidget(pixmap, basename(image_file), index)
                rec.deselected.connect(self.image_signal.myemit)
                self.multiple_image_layout.addItem(rec, row, col)
            else:
                self.single_image_scene.addPixmap(pixmap)

        adjusted=self.multiple_image_scene.itemsBoundingRect()
        adjusted.adjust(0,0,0,8*row)
        self.multiple_image_scene.setSceneRect(adjusted)





    def image_list_setSelected(self, index, select=True):
#        print("start image_list_setSelected")
        if select == True:
            self.page.listWidget.setCurrentRow(index, QItemSelectionModel.Select)
        else:
            self.page.listWidget.setCurrentRow(index, QItemSelectionModel.Toggle)
#        print("     fin image_list_setSelected")



    def image_list_update(self, images, shortcuts):
        """ Put all the images in the QListWidget """
        for index, image in images.items():
            item = ImageListItem()
            item.set_text(f'{basename(image)}')
            item.set_shortcuts_labels(shortcuts)
            item.set_index(index)
            item.set_icon(image)
            item.set_icon_size(60)

            self.page.listWidget.addItem(item)
            self.page.listWidget.setItemWidget(item, item.widget)

