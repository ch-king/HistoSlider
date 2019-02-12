from PyQt5.QtCore import QRectF
from pyqtgraph import ImageItem

from histoslider.image.slide_image import SlideImage


class SlideImageItem(ImageItem):
    """
    Expands the pyqtgraph ImageItem class to use a SlideImage in the background
    """
    def __init__(self, slide_image=None, **kargs):
        ImageItem.__init__(self, image=None, **kargs)
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

    def attach_image(self, img, RGB=True):
        self.slide_image.attach_image(img, RGB)
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
