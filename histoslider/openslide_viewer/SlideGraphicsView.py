from PyQt5.QtCore import QPoint, QRectF
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsView


class SlideGraphicsView(QGraphicsView):
    def __init__(self, scene, on_view_changed):
        super().__init__(scene)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.horizontalScrollBar().sliderMoved.connect(on_view_changed)
        self.verticalScrollBar().sliderMoved.connect(on_view_changed)

    def reset_view_transform(self):
        self.resetTransform()
        self.horizontalScrollBar().setValue(0)
        self.verticalScrollBar().setValue(0)

    def mouseDoubleClickEvent(self, event):
        point = self.mapToScene(event.pos())
        x = point.x()
        y = point.y()
        self.centerOn(x, y)
        super().mouseDoubleClickEvent(event)

    def get_current_view_scene_rect(self):
        return self.mapToScene(self.viewport().rect()).boundingRect()

    def get_current_view_scale(self):
        scale = self.transform().m11()
        return scale
