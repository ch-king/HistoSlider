from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QApplication

from utils.image_wrappers import GreyImageItem, SlideImageItem

__author__ = 'vitoz'


# general functions
def getDownsampleXYWH(xywh, current_downsample, target_downsample=1):
    """
    :param xywh: a touple of xywh
    :param current_downsample:
    :param target_downsample:
    :return:
    """

    (x, y, w, h) = (int(i * current_downsample / target_downsample) for i in xywh)
    return x, y, w, h


class ImageItem(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_item = GreyImageItem(parent=self)

    def loadImage(self, file, RGB=False):
        """

        :param file: get_filename or PIL object to be loaded
        :return bool: success of loading
        """
        # load the image
        try:
            self.image_item.load_image(filename=file)
            self.prepareGeometryChange()
        except:
            print('oo')
            return False

        self.scene().dirty = True

        return True

    def boundingRect(self):
        if self.image_item.image is not None:
            size = self.image_item.image.shape
        else:
            size = (0, 0)
        return QRectF(0, 0, size[0], size[1])

    def paint(self, *args, **kwargs):
        self.image_item.paint(*args, **kwargs)


class SlideItem(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_item = SlideImageItem(parent=self)

    def loadImage(self, file, RGB=True):
        """

        :param file: get_filename or PIL object to be loaded
        :return bool: success of loading
        """
        # load the image
        try:
            self.image_item.load_image(filename=file, RGB=RGB)
            self.prepareGeometryChange()
        except:
            print('oo')
            return False

        self.scene().dirty = True

        return True

    def update_content(self, x, y, w, h, downsample):
        # get new level
        level = self.image_item.slide_image.get_best_level_for_downsample(downsample)
        img_downsample = self.image_item.slide_image.level_downsamples()[level]

        #
        (wmax_level, hmax_level) = self.image_item.slide_image.level_dimensions[level]
        window_x = min(max(int(x), 0), wmax_level * img_downsample)
        window_y = min(max(int(y), 0), hmax_level * img_downsample)
        window_w = min(int(w / img_downsample), int(wmax_level - (window_x / img_downsample)))
        window_h = min(int(h / img_downsample), int(hmax_level - (window_y / img_downsample)))
        self.image_item.update_image_region(level, window_x, window_y, window_w, window_h)

        # at the moment the positioning is done on the level of the image_item
        # could also be done on on the graphitem level with self.setPos/setScale
        # (this might interfere with the way the positioning is handled lateron, so I dont do it on this level)
        self.image_item.setPos(window_x, window_y)
        self.image_item.setScale(img_downsample)

    def paint(self, *args, **kwargs):
        self.image_item.paint(*args, **kwargs)

    def boundingRect(self):
        size = self.image_item.slide_image.dimensions
        return QRectF(0, 0, size[0], size[1])


class SlideScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cur_downsample = 1
        self.cur_xywhds = (0, 0, 0, 0, 1)
        self.dirty = True

    def reset(self):
        # reset variables
        self.cur_downsample = 1
        self.cur_xywhds = (0, 0, 0, 0, 1)
        # remove the old pixelmap
        for item in self.items():
            self.removeItem(item)
        self.dirty = True

    def paint_view(self, view, x, y, w, h, downsample=None, wmax=100000, hmax=10000):
        if downsample is None:
            downsample = self.cur_downsample

        if ((x, y, w, h, downsample) == self.cur_xywhds) and not self.dirty:
            return
        else:
            self.cur_xywhds = (x, y, w, h, downsample)

        if self.cur_downsample == downsample:
            # only update objects if downsample does not change
            # as when upon change of zoom the window changes as well
            for item in self.items():
                if hasattr(item, 'update_content'):
                    item.update_content(x, y, w, h, downsample)

        if self.cur_downsample != downsample:
            view.scale(self.cur_downsample / downsample, self.cur_downsample / downsample)
            self.cur_downsample = downsample

        self.dirty = False


class SlideView(QGraphicsView):
    def __init__(self, scene, *args, zoomhandler=None, **kwargs):
        super().__init__(scene, *args, **kwargs)
        self.zoom_handler = None

    def setZoomhandler(self, zoomhandler):
        self.zoom_handler = zoomhandler

    def get_current_scene_window(self):
        size = self.size()
        points = self.mapToScene(0, 0, size.width(), size.height()).boundingRect()
        (x, y, w, h) = (points.x(), points.y(), points.width(), points.height())
        return x, y, w, h

    def updateSlideView(self):
        (x, y, w, h) = self.get_current_scene_window()
        self.scene().paint_view(self, x, y, w, h, self.scene().cur_downsample)

    def paintEvent(self, event):
        self.updateSlideView()
        super().paintEvent(event)

    def mouseDoubleClickEvent(self, event):
        point = self.mapToScene(event.pos())
        x = point.x()
        y = point.y()
        self.centerOn(x, y)
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        point = self.mapToScene(event.pos())
        x = point.x()
        y = point.y()
        print(x, y)
        event.ignore()
        super().mousePressEvent(event)

    def wheelEvent(self, event, *args, **kwargs):
        """

        :param event: QWheelEvent
        """

        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            super().wheelEvent(event, *args, **kwargs)
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
