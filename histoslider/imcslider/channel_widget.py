from PyQt5.QtCore import QAbstractTableModel, Qt

__author__ = 'vitoz'

class ChannelTableModel(QAbstractTableModel):
    """
    Makes a model wraper for a list of dicts. Each entry corresponds to a
    row, each dict entry to a column.
    """
    def __init__(self,  data_dict_list=None, dict_keys=None, parent=None, **kwrgs):
        super().__init__(parent, **kwrgs)

        if data_dict_list is None:
            data_dict_list = [{}]

        self.data_dict_list = data_dict_list
        if dict_keys is None:
            dict_keys = list(self.data_dict_list[0].keys())

        self.header = dict_keys
        self.keys = dict_keys

    def rowCount(self, parent):
        return len(self.data_dict_list)

    def columnCount(self, parent):
        return len(self.keys)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.data_dict_list[index.row()].get(self.keys[index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None


class ImageChannelTableModel(ChannelTableModel):
    """
    Makes a model wraper for a list of dicts. Each entry corresponds to a
    row, each dict entry to a column.
    """
    def __init__(self, image_item=None, parent=None, **kwrgs):
        data_dict_list = image_item.channels
        self.image_item = image_item

        super().__init__(data_dict_list=data_dict_list, parent=parent, **kwrgs)

    def get_filename(self, row):
        return self.image_item.get_filename(channel_idx=row)
