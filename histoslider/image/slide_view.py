import imctools.io.mcdparser as mcdparser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QWheelEvent
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QWidget, QMenu, QAction

from histoslider.core.hub_listener import HubListener
from histoslider.core.message import TreeViewCurrentItemChangedMessage
from histoslider.image.image_item import ImageItem
from histoslider.image.slide_item import SlideItem
from histoslider.models.channel_data import ChannelData
from histoslider.models.data_manager import DataManager


class SlideView(QGraphicsView, HubListener):
    def __init__(self, scene: QGraphicsScene, parent: QWidget):
        QGraphicsView.__init__(self, scene, parent)
        HubListener.__init__(self)
        self.setMinimumSize(200, 200)
        self.setAlignment(Qt.AlignCenter)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.openViewContextMenu)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.zoom_handler = None
        self.register_to_hub(DataManager.hub)

    def register_to_hub(self, hub):
        hub.subscribe(self, TreeViewCurrentItemChangedMessage, self._on_current_item_changed)

    def _on_current_item_changed(self, message: TreeViewCurrentItemChangedMessage):
        if isinstance(message.item, ChannelData):
            channel_data: ChannelData = message.item
            with mcdparser.McdParser(channel_data.slide.path) as mcd:
                acq = mcd.get_imc_acquisition(channel_data.acquisition.name, channel_data.acquisition.description)
                img = acq.get_img_by_label(channel_data.label)
                self.scene().clear()
                slide = True
                RGB = True
                if slide:
                    self.graphItem = SlideItem(scene=self.scene())
                    success = self.graphItem.loadImage(fname, RGB)

                else:
                    self.graphItem = ImageItem(scene=self.scene())
                    success = self.graphItem.loadImage(fname, RGB)

                if not success:
                    message = "Failed to load an image"
                else:
                    self.scene().setSceneRect(self.graphItem.boundingRect())
                    self.histogram.setImageItem(self.graphItem.image_item)
                    # self.histogram.autoHistogramRange()
                    self.showImage()

    def showImage(self, downsample=None):
        if self.scene().width() == 0:
            return
        if downsample is None:
            downsample = 1.15
        (x, y, w, h) = self.get_current_scene_window()

        self.scene().paint_view(self, x, y, w, h, downsample)

    def openViewContextMenu(self, position):
        tree_idxs = self.tree_widget.selectedIndexes()
        menu = QMenu()
        if len(tree_idxs) > 0:
            add_align_point = QAction(self)
            add_align_point.setText('Add align point')
            add_align_point.triggered.connect(lambda: self.tree_widget.model().add_align_point(parent_idx=tree_idxs[0],
                                                                                               position=position,
                                                                                               graph_item=self.graphItem,
                                                                                               view=self.view))
            menu.addAction(add_align_point)
        menu.exec_(self.view.mapToGlobal(position))

    def setZoomHandler(self, zoom_handler):
        self.zoom_handler = zoom_handler

    def get_current_scene_window(self):
        size = self.size()
        points = self.mapToScene(0, 0, size.width(), size.height()).boundingRect()
        (x, y, w, h) = (points.x(), points.y(), points.width(), points.height())
        return x, y, w, h

    def updateSlideView(self):
        (x, y, w, h) = self.get_current_scene_window()
        self.scene().paint_view(self, x, y, w, h, self.scene().cur_downsample)

    def paintEvent(self, event: QPaintEvent):
        self.updateSlideView()
        super().paintEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        point = self.mapToScene(event.pos())
        x = point.x()
        y = point.y()
        self.centerOn(x, y)
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        point = self.mapToScene(event.pos())
        x = point.x()
        y = point.y()
        print(x, y)
        event.ignore()
        super().mousePressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            super().wheelEvent(event)
        else:
            if self.zoom_handler is not None:
                curVal = self.zoom_handler.value()
                numDegrees = event.delta() / 8
                numSteps = numDegrees / 15
                if numSteps > 0:
                    zoom_val = max(curVal - curVal * 0.1 * numSteps, 0.001)
                else:
                    zoom_val = curVal - curVal * 0.1 * numSteps
                self.zoom_handler.setValue(zoom_val)
