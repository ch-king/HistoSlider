from histoslider.models import acquisition_2d_data
from histoslider.models.base_data import BaseData


class SlideData(BaseData):
    def __init__(self, name: str, tab_index: int):
        super().__init__(name)
        self.path: str = None
        self.tab_index = tab_index

    def add_acquisition2d(self, acquisition: acquisition_2d_data):
        self._add_child(acquisition)
