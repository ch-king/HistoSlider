from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QGraphicsScene


class SlideGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
