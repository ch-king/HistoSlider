from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem


class SelectedRectGraphicsItem(QGraphicsItem):
    def __init__(self, qrectf: QRectF):
        super().__init__()
        self.qrectf = qrectf
        self.setAcceptedMouseButtons(Qt.NoButton)

    def boundingRect(self):
        return self.qrectf

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None
    ):
        painter.save()
        pen = QPen(QColor(0, 0, 0, 255))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(self.qrectf)
        painter.restore()
