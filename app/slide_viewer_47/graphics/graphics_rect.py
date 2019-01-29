import typing

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QBrush, QPainter
from PySide2.QtWidgets import QWidget, QGraphicsRectItem, QStyleOptionGraphicsItem


class GraphicsRect(QGraphicsRectItem):
    def __init__(self, x_y_w_h, color: QColor):
        super().__init__(*x_y_w_h)
        self.x_y_w_h = x_y_w_h
        self.color = color
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setAcceptHoverEvents(False)
        self.brush = QBrush(self.color)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...):
        painter.save()
        painter.setBrush(self.brush)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawRect(*self.x_y_w_h)
        painter.restore()
