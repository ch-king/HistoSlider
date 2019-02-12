from PyQt5.QtGui import QIcon

from histoslider.image.helpers import SlideType
from histoslider.models.acquisition_data import AcquisitionData
from histoslider.models.base_data import BaseData


class SlideData(BaseData):
    def __init__(self, name: str, path: str, slide_type: SlideType):
        super().__init__(name)
        self.path = path
        self.slide_type = slide_type

    def add_acquisition(self, acquisition: AcquisitionData):
        self.addChild(acquisition)

    @property
    def icon(self):
        return QIcon(":/icons/icons8-sheets-16.png")

    @property
    def tooltip(self):
        return "Slide"
