from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from histoslider.image.grey_image_item import GreyImageItem


class ImageItem(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem = None):
        QGraphicsItem.__init__(self, parent)
        self.image_item = GreyImageItem(parent=self)

    def loadImage(self, file, RGB: bool = False):
        """
        :param file: get_filename or PIL object to be loaded
        :return bool: success of loading
        """
        # load the image
        try:
            self.image_item.load_image(filename=file)
            self.prepareGeometryChange()
        except Exception as e:
            print(e)
            return False

        return True

    def attachImage(self, img, RGB=True):
        """
        :param file: get_filename or PIL object to be loaded
        :return bool: success of loading
        """
        # load the image
        try:
            self.image_item.attach_image(img, RGB)
            self.prepareGeometryChange()
        except Exception as e:
            print(e)
            return False

        return True

    def boundingRect(self):
        if self.image_item.image is not None:
            size = self.image_item.image.shape
        else:
            size = (0, 0)
        return QRectF(0, 0, size[0], size[1])

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        self.image_item.paint(painter)
