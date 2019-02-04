import openslide
from PIL.ImageQt import ImageQt
from PySide2.QtCore import QRectF, QRect, Qt
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtGui import QPixmapCache
from PySide2.QtWidgets import (
    QGraphicsItem,
    QWidget,
    QStyleOptionGraphicsItem,
)


class TileGraphicsItem(QGraphicsItem):
    def __init__(self, x_y_w_h, slide_path: str, level: int, downsample: float):
        super().__init__()
        self.x_y_w_h = x_y_w_h
        self.slide_rect_0 = QRect(
            int(x_y_w_h[0] * downsample),
            int(self.x_y_w_h[1] * downsample),
            x_y_w_h[2],
            x_y_w_h[3],
        )
        self.slide_path = slide_path
        self.level = level
        self.downsample = downsample
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setAcceptHoverEvents(True)
        self.cache_key = slide_path + str(level) + str(self.slide_rect_0)
        # self.setCacheMode(QGraphicsItem.ItemCoordinateCache, self.slide_rect_0.size())
        # self.setFlag(QGraphicsItem.ItemClipsToShape, True)

    def pilimage_to_pixmap(self, pilimage):
        qim = ImageQt(pilimage)
        pix = QPixmap.fromImage(qim)
        return pix

    def boundingRect(self):
        return QRectF(0, 0, self.slide_rect_0.width(), self.slide_rect_0.height())

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None
    ):
        self.pixmap = QPixmapCache.find(self.cache_key)
        if not self.pixmap:
            with openslide.open_slide(self.slide_path) as slide:
                tile_pilimage = slide.read_region(
                    (self.slide_rect_0.x(), self.slide_rect_0.y()),
                    self.level,
                    (self.slide_rect_0.width(), self.slide_rect_0.height()),
                )
                self.pixmap = self.pilimage_to_pixmap(tile_pilimage)
                # self.pixmap.fill(Qt.red)
                QPixmapCache.insert(self.cache_key, self.pixmap)

        painter.drawPixmap(self.boundingRect().toRect(), self.pixmap)

    def __str__(self) -> str:
        return "{}: slide_path: {}, slide_rect_0: {}".format(
            self.__class__.__name__, self.slide_path, self.slide_rect_0
        )

    def __repr__(self) -> str:
        return self.__str__()
