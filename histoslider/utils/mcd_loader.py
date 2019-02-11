import os

import imctools.io.mcdparser as mcdparser

from histoslider.models.acquisition_data import AcquisitionData
from histoslider.models.channel_data import ChannelData
from histoslider.models.slide_data import SlideData


class McdLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        with mcdparser.McdParser(self.file_path) as mcd:
            file_name = os.path.basename(self.file_path)
            slide_data = SlideData(file_name, self.file_path)
            for id in mcd.acquisition_ids:
                description = mcd.get_acquisition_description(id)
                imc_ac = mcd.get_imc_acquisition(id, description)
                acquisition_data = AcquisitionData(imc_ac.image_ID, imc_ac.image_description)
                slide_data.add_acquisition(acquisition_data)
                for i in range(imc_ac.n_channels):
                    channel_data = ChannelData(imc_ac.channel_labels[i], imc_ac.channel_metals[i], imc_ac.channel_mass[i])
                    acquisition_data.add_channel(channel_data)
            return slide_data
