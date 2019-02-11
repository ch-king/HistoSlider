from typing import Union, Tuple

import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from openslide import AbstractSlide, open_slide, OpenSlide, ImageSlide

from histoslider.image.helpers import dummyImageDecorator


class SlideImage(AbstractSlide):
    # This class is a wrapper for the OpenSlide class in order to integrate it into a QT application
    def __init__(self):
        self.filename: str = None
        self.img: Union[OpenSlide, ImageSlide] = None
        self.RGB = True

    def load_slide(self, filename: str, RGB=True):
        # Loads a (slide) image
        self.filename = filename
        self.RGB = RGB
        # self.img will be an OpenSlide class image
        self.img = open_slide(filename)

    @dummyImageDecorator
    def read_region(self, location: Tuple[int, int], level: int, size: Tuple[int, int]) -> Image:
        """
        Returns a PIL image from the region

        :rtype : PIL image
        """

        rgba_image = self.img.read_region(location, level, size)
        return rgba_image

    @dummyImageDecorator
    def read_downsample_region(self, downsample: float, location: Tuple[int, int], size: Tuple[int, int]) -> Image:
        """
        Returns a PIL image directly using the best level for the downsample

        :rtype : PIL image
        """

        level = self.img.get_best_level_for_downsample(downsample)
        rgba_image = self.read_region(location, level, size)
        return rgba_image

    @dummyImageDecorator
    def read_level_region(self, level: int, location: Tuple[int, int], size: Tuple[int, int]) -> Image:
        """
        Returns a PIL image directly using the best level for the downsample

        :rtype : PIL image
        """

        rgba_image = self.read_region(location, level, size)
        return rgba_image

    def getPixmap(self, level: int, x: int, y: int, width: int, height: int) -> QPixmap:
        """
        :param level: zoom level
        :param x: x coordinates
        :param y: y coordinates
        :param width: window width
        :param height: window height
        :return: qt
        """
        img = self.read_level_region(level, (x, y), (width, height))
        img_qt = ImageQt(img)
        pixmap = QPixmap.fromImage(img_qt)
        return pixmap

    def getNumpyImage(self, level: int, x: int, y: int, width: int, height: int):
        """
        :param level: zoom level
        :param x: x coordinates
        :param y: y coordinates
        :param width: window width
        :param height: window height
        :return: qt
        """
        img = self.read_level_region(level, (x, y), (width, height))
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

    def get_best_level_for_downsample(self, downsample: float):
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
