from histoslider.models import Acquisition2DData
from histoslider.models.BaseData import BaseData


class SlideData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)
        self.path: str = None

    def add_acquisition2d(self, acquisition: Acquisition2DData):
        self._add_child(acquisition)
