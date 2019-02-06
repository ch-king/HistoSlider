from histoslider.models import SlideData
from histoslider.models.BaseData import BaseData


class WorkspaceData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)
