import ctypes

import numpy as np
from PIL import Image
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage, QPixmap
from openslide import AbstractSlide, open_slide
from pyqtgraph import ImageItem

from utils.helpers import dummyImageDecorator


class SlideImage(AbstractSlide):
    # This class is a wrapper for the OpenSlide class in order
    # to integrate it into a QT application
    def __init__(self):
        self.filename = None
        self.img = None
        self.RGB = True

    def load_slide(self, filename, RGB=True):
        # Loads a (slide) image
        self.RGB = RGB
        # self.img will be an OpenSlide class image
        self.img = open_slide(filename)
        self.filename = filename

    @dummyImageDecorator
    def read_region(self, location, level, size):
        """
        Returns a PIL image from the region

        :rtype : PIL image
        """

        timg = self.img.read_region(location, level, size)

        return timg

    @dummyImageDecorator
    def read_downsample_region(self, downsample, location, size):
        """
        Returns a PIL image directly using the best level for the downsample

        :rtype : PIL image
        """

        level = self.img.get_best_level_for_downsample(downsample)
        timg = self.read_region(location, level=level, size=size)

        return timg

    @dummyImageDecorator
    def read_level_region(self, level, location, size):
        """
        Returns a PIL image directly using the best level for the downsample

        :rtype : PIL image
        """

        timg = self.read_region(location, level=level, size=size)

        return timg

    def getPixmap(self, level, window_x, window_y, window_w, window_h):
        """

        :param level: zoom level
        :param window_x: x coordinates
        :param window_y: y coordinates
        :param window_w: window width
        :param window_h: window height
        :return: qt
        """
        img = self.read_level_region(level, (window_x, window_y), (window_w, window_h))
        # causes a memory leak
        # img = ImageQt.ImageQt(img)

        # fix (but switches r and b)
        data = img.tostring('raw', 'RGBA')
        img = QImage(data, img.size[0], img.size[1], QImage.Format_ARGB32)
        ctypes.c_long.from_address(id(data)).value = 1
        pixmap = QPixmap.fromImage(img)
        return pixmap

    def getNumpyImage(self, level, window_x, window_y, window_w, window_h):
        """

        :param level: zoom level
        :param window_x: x coordinates
        :param window_y: y coordinates
        :param window_w: window width
        :param window_h: window height
        :return: qt
        """
        img = self.read_level_region(level, (window_x, window_y), (window_w, window_h))
        # convert the image to an array
        if self.RGB:
            img_array = np.asarray(img)
        else:
            img_array = np.asarray(img)[:, :, 0]
        img_array = img_array.swapaxes(0, 1)
        return img_array

    @property
    def dimensions(self):
        if self.img is None:
            return (0, 0)
        else:
            return self.img.dimensions

    @property
    def level_dimensions(self):
        if self.img is None:
            return (0, 0)
        else:
            return self.img.level_dimensions

    def dummy_image(self, mode='RGBA', size=(512, 512), color=0):
        """

        :rtype : PIL image
        """
        return Image.new('RGBA', size, color)

    def get_best_level_for_downsample(self, downsample):
        if self.img is not None:
            return self.img.get_best_level_for_downsample(downsample)
        else:
            return 0

    def level_downsamples(self):
        if self.img is not None:
            return self.img.level_downsamples
        else:
            return [1]

    def close(self):
        if self.img is not None:
            self.img.close()


class SlideImageItem(ImageItem):
    """
    Expands the pyqtgraph imageitem class to use a slideimage in the background
    """

    def __init__(self, slide_image=None, **kargs):
        super().__init__(image=None, **kargs)
        self.setPxMode(False)
        self.pos = (0, 0)
        self.scale = 1
        self.RGB = False
        self.setAutoDownsample(False)

        if slide_image is None:
            self.slide_image = SlideImage()
        else:
            self.slide_image = slide_image

    def load_image(self, filename, RGB=True):
        self.slide_image.load_slide(filename, RGB)
        self.RGB = RGB

    def update_image_region(self, level, window_x, window_y, window_w, window_h, autoLevels=False, **kargs):
        img = self.slide_image.getNumpyImage(level, window_x, window_y, window_w, window_h)
        self.setImage(image=img, autoLevels=autoLevels, **kargs)
        self.qimage = None

    # def render(self):
    #     super().render()
    #     w = int(self.image.shape[0]*self.scale)
    #     h = int(self.image.shape[1]*self.scale)
    #     self.qimage = self.qimage.scaled(w, h, qc.Qt.IgnoreAspectRatio, qc.Qt.FastTransformation)

    def setPos(self, window_x, window_y):
        self.pos = (window_x, window_y)

    def setScale(self, scale):
        self.scale = scale

    def paint(self, p, *args):
        if self.image is None:
            return
        if self.qimage is None:
            if self.RGB:
                self.lut = None
            self.render()
            if self.qimage is None:
                return
        if self.paintMode is not None:
            p.setCompositionMode(self.paintMode)

        p.drawImage(
            QRectF(self.pos[0], self.pos[1], self.image.shape[0] * self.scale, self.image.shape[1] * self.scale),
            self.qimage)


class GreyImageItem(ImageItem):
    def __init__(self, image=None, filename=None, **kargs):
        super().__init__(image=None, **kargs)
        self.setPxMode(False)
        self.setAutoDownsample(False)
        self.image = image

        if filename is not None:
            self.load_image(filename)

    def load_image(self, filename):
        img = Image.open(filename)
        self.image = np.asarray(img, dtype=np.float32).T
