from histoslider.models.base_data import BaseData


class MultiplexAcquisition2DData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)
        self.path: str = None
        self.channels = None
