from histoslider.models.base_data import BaseData
from histoslider.models.roi_data import RoiData


class PanoramaData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)

    def add_roi(self, roi: RoiData):
        self.addChild(roi)
