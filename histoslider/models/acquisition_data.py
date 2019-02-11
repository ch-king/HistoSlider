from histoslider.models.base_data import BaseData
from histoslider.models.channel_data import ChannelData


class AcquisitionData(BaseData):
    def __init__(self, name: str, description: str):
        super().__init__(name)
        self.description = description

    def add_channel(self, channel: ChannelData):
        self.addChild(channel)

    @property
    def slide(self):
        return self.parent()
