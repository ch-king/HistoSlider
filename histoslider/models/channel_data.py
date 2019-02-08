from histoslider.models.base_data import BaseData


class ChannelData(BaseData):
    def __init__(self, name: str, prefix: str):
        super().__init__(name)
        self.prefix = prefix
