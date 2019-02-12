import numpy as np
from PIL import Image
from pyqtgraph import ImageItem


class GreyImageItem(ImageItem):
    def __init__(self, image=None, filename=None, **kargs):
        ImageItem.__init__(self, image, **kargs)
        self.setPxMode(False)
        self.setAutoDownsample(False)
        self.image = image

        if filename is not None:
            self.load_image(filename)

    def load_image(self, file_path: str):
        img = Image.open(file_path)
        self.image = np.asarray(img, dtype=np.float32).T

    def attach_image(self, img):
        self.image = np.asarray(img, dtype=np.float32).T
