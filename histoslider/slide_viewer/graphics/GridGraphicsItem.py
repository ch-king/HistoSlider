from itertools import starmap

from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget


class GridGraphicsItem(QGraphicsItem):
    def __init__(
        self,
        grid_rects_0_level: int,
        color_alphas,
        bounding_rect,
        base_color_rgb=(0, 255, 0),
    ):
        super().__init__()
        self.grid_rects_0_level = grid_rects_0_level
        self.color_alphas = color_alphas
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setAcceptHoverEvents(False)
        self.bounding_rect = bounding_rect
        self.base_color_rgb = base_color_rgb

        # self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.downsample = 1

        self.star_map_ = starmap

        self.color_alpha_rects_0_level = {}
        for color_alpha, grid_rect_0_level in zip(color_alphas, grid_rects_0_level):
            self.color_alpha_rects_0_level.setdefault(color_alpha, []).append(
                grid_rect_0_level
            )

        self.recompute_bounding_rect()

    def recompute_bounding_rect(self):
        self.bounding_qrectf = QRectF(
            self.bounding_rect[0],
            self.bounding_rect[1],
            self.bounding_rect[2] / self.downsample,
            self.bounding_rect[3] / self.downsample,
        )

    def update_downsample(self, downsample):
        self.downsample = downsample
        self.recompute_bounding_rect()

    def boundingRect(self):
        return self.bounding_qrectf

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None
    ):
        painter.save()
        scale = 1 / self.downsample
        painter.scale(scale, scale)

        for color_alpha, rects in self.color_alpha_rects_0_level.items():
            color = QColor(*self.base_color_rgb, color_alpha)
            painter.setBrush(color)
            qrectfs = self.star_map_(QRectF, rects)
            painter.drawRects(list(qrectfs))

        painter.restore()
