from PySide2.QtWidgets import QGraphicsView


class SlideGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)

    def mouseDoubleClickEvent(self, event):
        point = self.mapToScene(event.pos())
        x = point.x()
        y = point.y()
        self.centerOn(x, y)
        super().mouseDoubleClickEvent(event)
