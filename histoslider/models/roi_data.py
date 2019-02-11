from histoslider.models.base_data import BaseData
from histoslider.models.acquisition_data import AcquisitionData


class RoiData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)

    def add_acquisition(self, stack: AcquisitionData):
        self.addChild(stack)
