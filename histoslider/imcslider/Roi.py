import numpy as np
from PyQt5.QtCore import QRectF, QSizeF, Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsItem


def eukledian_dist(pointA, pointB):
    d = np.sqrt(np.sum(pow(pointA.x() - pointB.x(), 2) + pow(pointA.y() - pointB.y(), 2)))
    return d


class RoiCircle(QGraphicsItem):

    def __init__(self, rect, parent, view):
        super().__init__(parent)
        self.rect = rect
        self.getHandleFromRect()
        self.setFlags(QGraphicsItem.ItemIsFocusable)
        self.handle_is_pressed = False

        self.minsize = 2

    def getHandleFromRect(self):
        x = self.rect.x()
        y = self.rect.y()
        w = 0.2 * self.rect.height()
        h = 0.2 * self.rect.width()
        self.resize_handle = QRectF(x, y, w, h)

    def center(self):
        return self.rect.center()

    def boundingRect(self):
        r = QRectF(1, 1, 1, 1)
        r.setSize(QSizeF(self.rect.width() * 1.1, self.rect.height() * 1.1))
        r.moveCenter(self.rect.center())
        return r

    def paint(self, painter, option, widget):
        pen = QPen()
        pen.setWidth(self.rect.width() / 30)
        pen.setBrush(Qt.red)
        painter.setPen(pen)
        painter.drawEllipse(self.rect)
        pen = QPen()
        pen.setWidth(self.rect.width() / 20)
        pen.setBrush(Qt.green)
        painter.setPen(pen)
        painter.drawEllipse(self.resize_handle)

    def mousePressEvent(self, event):

        if not self.handle_is_pressed:
            self.mousePressPos = event.scenePos()

        if self.resize_handle.contains(event.scenePos()):
            self.handle_is_pressed = True

        event.accept()

    def mouseMoveEvent(self, event):
        if self.handle_is_pressed:
            self.prepareGeometryChange()
            print(self.center())
            oldd = eukledian_dist(self.mousePressPos, self.center())
            newd = eukledian_dist(event.scenePos(), self.center())
            d = newd - oldd
            d *= 2
            self.mousePressPos = event.scenePos()
            oldCenter = self.rect.center()
            self.rect.setSize(
                QSizeF(max(self.rect.width() + d, self.minsize), max(self.rect.height() + d, self.minsize)))
            self.rect.moveCenter(oldCenter)
            self.getHandleFromRect()
            self.update()
        else:
            self.prepareGeometryChange()
            self.rect.moveCenter(event.scenePos())
            self.getHandleFromRect()
            self.update()

        event.accept()

    def mouseReleaseEvent(self, event):
        if self.handle_is_pressed:
            self.handle_is_pressed = False
            event.accept()
        else:
            self.prepareGeometryChange()
            self.rect.moveCenter(event.scenePos())
            self.getHandleFromRect()
            self.update()
