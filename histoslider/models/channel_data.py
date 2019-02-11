from histoslider.models.acquisition_data import AcquisitionData
from histoslider.models.base_data import BaseData
from histoslider.models.slide_data import SlideData


class ChannelData(BaseData):
    def __init__(self, label: str, metal: str, mass: int):
        super().__init__(label)
        self.label = label
        self.metal = metal
        self.mass = mass

    @property
    def acquisition(self) -> AcquisitionData:
        return self.parent()

    @property
    def slide(self) -> SlideData:
        return self.acquisition.slide
