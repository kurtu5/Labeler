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
from PySide2.QtWidgets import QApplication, QStackedWidget, QCheckBox, QComboBox
from PySide2.QtGui import QTransform, QWindow, QPalette, QColor, QPainter


import time
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
            label_w = QLabel(f'{label}')
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
        

            
class SelectionWidget(QWidget):
    select = Signal(dict)
    noselect = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected = {}  # shortcut => {widget => checked}
        self.start()

    def start(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(QLabel("Select images without features set"), 0,0,1,0)
        self.setLayout(self.grid_layout)
        self.selectionButton=QPushButton("Select")
        self.selectionButton.clicked.connect(self.emitter)
        self.noSelectionButton=QPushButton("No Select")
        self.noSelectionButton.clicked.connect(self.noselect.emit)


    def emitter(self):
#        print("emit a signal")
        shortcut_emit = {}
        for shortcut, checked_w in self.selected.items():
#            print(f'{shortcut}={checked_w.isChecked()}')
            shortcut_emit[shortcut] = checked_w.currentText()
        self.select.emit(shortcut_emit)

    def set_shortcuts_labels(self, shortcuts_labels):
        col = 0
        row = 1
        for shortcut, label in shortcuts_labels.items():
            row += 1
            features = {-1,0,1,10}
            combo_w = QComboBox()
            for feature in features:
                combo_w.addItem(str(feature))
            
            label_w = QLabel(f'{label}')
            self.selected[shortcut] = combo_w
#            self.pal.setColor(QPalette.WindowText, self.feature.unknown)
#            shortcut_w.setPalette(self.pal)
#            self.shortcuts[shortcut] = {'status': '', 'widget': shortcut_w  }
            self.grid_layout.addWidget(combo_w, row, col)
            self.grid_layout.addWidget(label_w, row, col+1)
        self.grid_layout.addWidget(self.selectionButton)
        self.grid_layout.addWidget(self.noSelectionButton)


class DisplayWidget(QStackedWidget):
    imageClicked = Signal(int, QEvent)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_columns = None  # Set when presenter starts # Max cols for multimages
        self.cached_images = {} # Cache read of image from disk

        self.start()


    def emitter(self, index, event):
        self.imageClicked.emit(index, event)
            
    def start(self):
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

        self.addWidget(self.single_image)
        self.addWidget(self.multiple_image)
        
    def setMaxColumns(self, max_cols):
        self.max_columns = max_cols
        
    def images_load(self, images):
        """ Take list of images and display in main window """
        num = len(images)
        if num == 0:
            return

        width=self.width()
        maxcol = self.max_columns
        if num < maxcol:
            maxcol = num
        colwidth = width/maxcol

        # Set proper widget for display of multiple or single images
        if num > 1:
            self.setCurrentWidget(self.multiple_image)
            # Clear the layout
            while self.multiple_image_layout.count():
                self.multiple_image_layout.removeAt(0)
            # Clear the scene
            for child in self.panel.childItems():
                child.setParent(None)
        else:
            self.setCurrentWidget(self.single_image)
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
                rec.imageClicked.connect(self.emitter)
                self.multiple_image_layout.addItem(rec, row, col)
            else:
                self.single_image_scene.addPixmap(pixmap)

        adjusted=self.multiple_image_scene.itemsBoundingRect()
        adjusted.adjust(0,0,0,8*row)
        self.multiple_image_scene.setSceneRect(adjusted)

class MultiImageWidget(QGraphicsWidget):
    imageClicked = Signal(int, QEvent)
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
        self.imageClicked.emit(self.index, event)

        return
#        print("Hover", event.type())
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



class ImageListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def setSelected(self, index, select=True):
        if select == True:
            self.setCurrentRow(index, QItemSelectionModel.Select)
        else:
            self.setCurrentRow(index, QItemSelectionModel.Deselect)
            
    def update(self, images, shortcuts, features):
        """ Put all the images in the QListWidget """

        self.clear()
        for index, image in images.items():
            item = ImageListItem()
            item.set_text(f'{basename(image)}')
            item.set_shortcuts_labels(shortcuts)
            feature = features[index]
            for shortcut in shortcuts.keys():
                item.set_shortcuts_status(shortcut, feature.get(shortcut))
            item.set_index(index)
            item.set_icon(image)
            item.set_icon_size(60)

            self.addItem(item)
            self.setItemWidget(item, item.widget)
            
            
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



#https://github.com/tpgit/MDIImageViewer seems to do everything....
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
import MVPBase

class View(MVPBase.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
            # Since I have default implemetations for showable pages, do this in base?
            path = os.path.dirname(os.path.realpath(__file__)) + "\\"
            file = QFile(path + "labeler.ui")
            file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.page = loader.load(file)

            # I could just modify the ui file.... but lets play with this
            self.page.horizontalLayout.removeWidget(self.page.display)
            self.page.display.close()
            self.page.display=DisplayWidget()
            self.page.horizontalLayout.insertWidget(1,self.page.display)

            self.page.horizontalLayout.removeWidget(self.page.listWidget)
            self.page.listWidget.close()
            self.page.listWidget=ImageListWidget()
            self.page.horizontalLayout.insertWidget(2,self.page.listWidget)
            self.page.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

            self.page.leftColumn.removeWidget(self.page.labelerWidget)
            self.page.labelerWidget.close()
            self.page.labelerWidget=LabelerWidget()
            self.page.leftColumn.insertWidget(1,self.page.labelerWidget)

            self.page.leftColumn.removeWidget(self.page.selectionWidget)
            self.page.selectionWidget.close()
            self.page.selectionWidget=SelectionWidget()
            self.page.leftColumn.insertWidget(2,self.page.selectionWidget)

            self.page_index = self.parent.stacked_widget.addWidget(self.page)
            self.page.columns_choice.setRange(1,10)

            # Global key press eventFilter.signal emits
            self.keyEvent = KeyEventFilter()
            self.parent.parent.installEventFilter(self.keyEvent)

    def max_columns_choice(self, choice):
        self.page.display.setMaxColumns(choice)
        self.page.columns_choice.setValue(choice)

    def labeler_widget_load(self):
        pass

    def images_load(self, images):
        self.page.display.images_load(images)

    def image_list_update(self, images, shortcuts, features):
        """ Put all the images in the QListWidget """
        self.page.listWidget.update(images, shortcuts, features)
   