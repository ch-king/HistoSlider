import typing

from PyQt5.QtCore import QRectF, Qt, QSize
from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem


class SelectedGraphicsRect(QGraphicsItem):
    def __init__(self, qrectf: QRectF):
        super().__init__()
        self.qrectf = QRectF(qrectf)
        self.setAcceptedMouseButtons(Qt.NoButton)

    def boundingRect(self):
        return self.qrectf

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        painter.save()
        pen = QPen(QColor(0, 0, 0, 255))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(self.qrectf)
        painter.restore()
