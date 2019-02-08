from histoslider.models import slide_data
from histoslider.models.base_data import BaseData


class WorkspaceData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)
