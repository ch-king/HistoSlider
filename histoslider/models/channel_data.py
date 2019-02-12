from PyQt5.QtGui import QIcon

from histoslider.models.base_data import BaseData


class ChannelData(BaseData):
    def __init__(self, label: str, metal: str, mass: int):
        super().__init__(label)
        self.label = label
        self.metal = metal
        self.mass = mass

    @property
    def acquisition(self):
        return self.parent()

    @property
    def slide(self):
        return self.acquisition.slide

    @property
    def icon(self):
        return QIcon(":/icons/icons8-compact-camera-16.png")

    @property
    def tooltip(self):
        return "Channel"
