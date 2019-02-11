from histoslider.imcslider.data_classes import SlideData
from histoslider.models.base_data import BaseData


class WorkspaceData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)

    def add_slide(self, slide: SlideData):
        self.addChild(slide)
