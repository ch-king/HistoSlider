from histoslider.models.BaseData import BaseData


class ChannelData(BaseData):
    def __init__(self, name: str, prefix: str):
        super().__init__(name)
        self.prefix = prefix
