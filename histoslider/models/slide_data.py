from histoslider.models.acquisition_data import AcquisitionData
from histoslider.models.base_data import BaseData
from histoslider.models.panorama_data import PanoramaData


class SlideData(BaseData):
    def __init__(self, name: str, path: str):
        super().__init__(name)
        self.path = path

    def add_panorama(self, panorama: PanoramaData):
        self.addChild(panorama)

    def add_acquisition(self, acquisition: AcquisitionData):
        self.addChild(acquisition)
