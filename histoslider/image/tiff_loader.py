import os

from histoslider.image.helpers import SlideType
from histoslider.models.slide_data import SlideData


class TiffLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        file_name = os.path.basename(self.file_path)
        slide_data = SlideData(file_name, self.file_path, SlideType.TIFF)
        return slide_data
