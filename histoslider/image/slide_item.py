from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from histoslider.image.slide_image_item import SlideImageItem


class SlideItem(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem = None):
        QGraphicsItem.__init__(self, parent)
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
        except Exception as e:
            print(e)
            return False

        self.scene().dirty = True

        return True

    def attachImage(self, img, RGB=True):
        """
        :param file: get_filename or PIL object to be loaded
        :return bool: success of loading
        """
        # load the image
        try:
            self.image_item.load_image(filename=file, RGB=RGB)
            self.prepareGeometryChange()
        except Exception as e:
            print(e)
            return False

        return True

    def update_content(self, x, y ,w, h, downsample):
        # get new level
        level = self.image_item.slide_image.get_best_level_for_downsample(downsample)
        img_downsample = self.image_item.slide_image.level_downsamples()[level]

        #
        (wmax_level, hmax_level) = self.image_item.slide_image.level_dimensions[level]
        window_x = min(max(int(x),0),wmax_level*img_downsample)
        window_y = min(max(int(y),0), hmax_level*img_downsample)
        window_w = min(int(w / img_downsample), int(wmax_level-(window_x/ img_downsample)))
        window_h = min(int(h / img_downsample), int(hmax_level-(window_y/ img_downsample)))
        self.image_item.update_image_region(level, window_x, window_y, window_w, window_h)

        # at the moment the positioning is done on the level of the image_item
        # could also be done on on the graphitem level with self.setPos/setScale
        # (this might interfere with the way the positioning is handled lateron, so I dont do it on this level)
        self.image_item.setPos(window_x, window_y)
        self.image_item.setScale(img_downsample)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        self.image_item.paint(painter)

    def boundingRect(self):
        size = self.image_item.slide_image.dimensions
        return QRectF(0, 0, size[0], size[1])
