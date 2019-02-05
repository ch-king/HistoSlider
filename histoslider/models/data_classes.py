import os
import re
import uuid

from PyQt5.QtCore import Qt

from utils.helpers import default_value, IdBasedProperty

"""
Hierarchy:
Project -> Experiment -> Slide -> ROI
"""


class AbstractData:
    """
    Defines the basic data class for entries.
    """

    data_type = None
    attribute_types = None

    def __init__(self, id=None, name=None, entry_dict=None,
                 parent_ids=None, add_data=None, checked=False):
        """
        Initializes the abstract add_data
        :rtype : object
        :param id: a hashable id
        :param name: a string
        :param entry_dict: a dictionary that contains all the entries
        :param parent_ids: ids of the parent of the entry
        :param children_ids: ids of the children of the entry
        :return:
        """
        if id is None:
            id = uuid.uuid4().int
        if entry_dict is None:
            entry_dict = dict()

        if parent_ids is None:
            parent_ids = list()

        if add_data is None:
            add_data = dict()

        self.id = id
        self.name = default_value(name, 'unnamed ' + str(self.id))

        entry_dict.update({id: self})
        self.entry_dict = entry_dict

        self.parent_ids = list(parent_ids)
        self.children_ids = list()

        self.column_names = ['data_type', 'name', 'show']
        self.column_flags = [Qt.ItemIsEnabled | Qt.ItemIsSelectable,
                             Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable,
                             Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEditable]
        self.item_data = add_data
        self.item_data.update({'data_type': self.data_type, 'name': self.name, 'show': None, 'checked': checked})

        if parent_ids != list():
            for par in self.parents:
                par.children_ids.append(self.id)

        self.graph_item = None

        if self.attribute_types is None:
            self.attribute_types = dict()
        self.attribute_types.update({'data_type': 'str', 'name': 'str', 'show': None})

    # property to get all children/parents
    parents = IdBasedProperty('parent_ids', 'entry_dict')
    children = IdBasedProperty('children_ids', 'entry_dict')

    def dump(self):
        '''
        Returns a dictionary with all the data of the item
        :return: a dict
        '''
        dumpdata = dict()
        dumpdata['data_type'] = self.data_type
        dumpdata['name'] = self.name
        dumpdata['id'] = self.id
        dumpdata['parent_ids'] = self.parent_ids
        dumpdata['data'] = dict()
        return dumpdata

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children_ids)

    def parentCount(self):
        return len(self.parent_ids)

    def childNumber(self, parent_nr=0):
        if parent_nr > self.parentCount():
            return self.parents.children.index(self)
        return 0

    def columnCount(self):
        return len(self.column_names)

    def data(self, column):
        return self.item_data[self.column_names[column]]

    def setData(self, column, value):
        at_name = self.column_names[column]
        at_type = self.attribute_types.get(at_name)
        if at_type == 'str':
            value = str(value)
            ok = True
        elif at_type == 'int':
            value, ok = value.toInt()
        elif at_type == 'bool':
            value = bool(value)
            ok = True
        if ok:
            self.item_data[at_name] = value

        return ok

    def flags(self, column):
        return self.column_flags[column]

    def parent(self, parent_nr=0):
        return self.parents[parent_nr]

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.children_ids):
            return False

        for row in range(count):
            self.children_ids.pop(position)

        return True

    def checked(self):
        return self.item_data['checked']

    def set_checked(self, state):
        self.item_data['checked'] = state
        return True

    def _find_parent_graph_item(self, itemList=None):
        if itemList is None:
            itemList = list()
            isTop = True
        else:
            isTop = False

        for parent in self.parents:
            if parent.graph_item is None:
                parent._fint_parent_graph_item(self, itemList)
            else:
                itemList.append(parent)
                if isTop:
                    return itemList

    def generate_graphics_item(self, parent=None, scene=None):
        gi = qg.QGraphicsItem(parent=parent, scene=scene)
        self.graph_item = gi
        return True


class RootData(AbstractData):
    def __init__(self, id=0, name='name', data_type='type', entry_dict=None):
        self.data_type = data_type
        super().__init__(id=id, name=name, entry_dict=entry_dict)

    def dump(self):
        pass


class ProjectData(AbstractData):
    """
    The class for project data
    """
    data_type = 'project'


class ExperimentData(AbstractData):
    """
    The class for experiment data, corresponds e.g. to a paraffin block
    """
    data_type = 'experiment'


class AbstractAreaData(AbstractData):
    """
    Abstract Dataclass with a shape and an image scale
    """
    data_type = 'AbstractArea'

    def __init__(self, shape=None, img_scale=None, transformation_matrix=None, data=None, **kwargs
                 ):
        """

        :param id:
        :param name:
        :param entry_dict:
        :param parent_ids:
        :param children_ids:
        :param transformation_matrix: dict with scale, rotation, move_xy: relation to parent
        :return:
        """

        if data is None:
            data = kwargs.get('data')
        if data is None:
            data = dict()

        super(AbstractAreaData, self).__init__(add_data=data, **kwargs)

        if shape is None:
            shape = data.get('shape')

        if img_scale is None:
            img_scale = data.get('img_scale')

        if transformation_matrix is None:
            transformation_matrix = data.get('transformation_matrix')

        self.shape = shape
        self.img_scale = img_scale
        self.transformation_matrix = transformation_matrix

    def dump(self):
        dumpdata = super().dump()
        dumpdata['data']['transformation_matrix'] = self.transformation_matrix
        dumpdata['data']['shape'] = self.shape
        dumpdata['data']['img_scale'] = self.img_scale
        return dumpdata


class SlideData(AbstractAreaData):
    """
    The class that represents a physical slide
    """
    data_type = 'slide'


class AcquisitionContainer(AbstractAreaData):
    data_type = 'acquisition_container'


class AcquisitionData2D(AbstractAreaData):
    """
    Abstract class to represent 2D aquisition data
    """

    data_type = 'acquisition_2d'

    def __init__(self, file_directory=None, base_name=None, slide=False, file_extension='.tif',
                 name_seperator='_',
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.file_directory = file_directory
        self.base_name = base_name

        self.RGB = True
        self.slide = slide

        self._file_extension = file_extension
        self._name_seperator = name_seperator

    def get_filename(self):
        return os.path.join(self.file_directory,
                            self.base_name +
                            self._file_extension)

    def dump(self):
        dumpdata = super().dump()
        dumpdata['data']['file_extension'] = self._file_extension
        dumpdata['data']['file_directory'] = self.file_directory
        dumpdata['data']['base_name'] = self.base_name
        dumpdata['data']['slide'] = self.slide
        return dumpdata


class MultiplexAcquisitionData2D(AcquisitionData2D):
    """
    MultiplexAcquisitionData2D:
    Additional:
    - channels: List of dicts containing at least
        - 'channel_name': the channel name (description)
        - 'channel_prefix': the prefix at of the channel name used to construct the get_filename
    """
    data_type = 'multiplex_acquisition_2d'

    def __init__(self, channels=None, **kwargs
                 ):

        super().__init__(**kwargs)

        if channels is None:
            channels = list()

        self.channels = channels

        self.RGB = False

    def get_filename(self, channel_idx=0, sep=None):
        if sep is None:
            sep = self._name_seperator

        filename = self.base_name + sep + self.channels[channel_idx]['channel_prefix'] + self._file_extension
        if filename[0] == sep:
            filename = filename[1:]

        return os.path.join(self.file_directory, filename)

    def dump(self):
        dumpdata = super().dump()
        dumpdata['data']['channels'] = self.channels
        return dumpdata


class RoiContainer(AbstractAreaData):
    data_type = 'ROI'


class AlignPointsContainer(RoiContainer):
    data_type = 'align_points_container'


class AlignPoints(RoiContainer):
    data_type = 'align_point'

    def __init__(self, position,
                 **kwargs):
        self.position = position

        super().__init__(**kwargs)

    def dump(self):
        dumpdata = super().dump()
        dumpdata['data']['position'] = self.position


# Functions to handle the data

def data_parser(data_list, root_item=None):
    """
    Reads all data entries specified in a list data_list.
    :param data_list:
    :return: an entry dict with the parsed tree structure
    """
    data_list = data_list.copy()
    if root_item is None:
        root_id = list()
        entry_dict = dict()
    else:
        root_id = [root_item.id]
        entry_dict = root_item.entry_dict

    for entry in data_list:
        entry_type = entry.pop('data_type')

        if entry.get('id') in entry_dict.keys():
            raise ValueError("Duplicated id in data_list!")

        if entry.get('parent_ids') is None:
            entry.update({'parent_ids': root_id})

        if entry_type == 'project':
            ProjectData(entry_dict=entry_dict,
                        parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                        **entry['data'])

        elif entry_type == 'experiment':
            ExperimentData(entry_dict=entry_dict,
                           parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                           **entry['data'])

        elif entry_type == 'slide':
            SlideData(entry_dict=entry_dict,
                      parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                      **entry['data'])

        elif entry_type == 'acquisition_2d':
            AcquisitionData2D(entry_dict=entry_dict,
                              parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                              **entry['data'])

        elif entry_type == 'bf_acquisition':
            AcquisitionData2D(entry_dict=entry_dict,
                              parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                              **entry['data'])


        elif entry_type == 'multiplex_acquisition_2d':
            if entry['data'].get('channels') is None:
                files = os.listdir(entry['data']['file_directory'])
                extension = entry['data']['file_extension']
                extlen = len(extension)
                filenames = [f.replace(extension, '') for f in files if f[-extlen:] == extension]
                channames = [f.rpartition('(')[0] for f in filenames]
                metalnames = list()
                masslist = list()
                for f in filenames:
                    part = f.rpartition('(')
                    if len(part) >= 3:
                        metal = part[2].rpartition(')')[0]
                        try:
                            mass = int(re.search('[0-9]+', metal).group(0))
                        except:
                            mass = 0
                    else:
                        metal = ''
                        mass = 0
                    metalnames.append(metal)
                    masslist.append(mass)

                channel_list = [{'channel_prefix': f, 'channel_name': cn, 'metal': m, 'mass': ma} for f, cn, m, ma in
                                zip(filenames, channames, metalnames, masslist)]
                entry['data'].update({'channels': channel_list})
            MultiplexAcquisitionData2D(entry_dict=entry_dict,
                                       parent_ids=entry['parent_ids'], id=entry['id'],
                                       name=entry['name'],
                                       **entry['data'])

        elif entry_type == 'acquisition_container':
            AcquisitionContainer(entry_dict=entry_dict,
                                 parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                                 **entry['data'])

        elif entry_type == 'align_points_container':
            AlignPointsContainer(entry_dict=entry_dict,
                                 parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                                 **entry['data'])

        elif entry_type == 'align_point':
            AlignPoints(entry_dict=entry_dict,
                        parent_ids=entry['parent_ids'], id=entry['id'], name=entry['name'],
                        **entry['data'])
        else:
            raise NotImplementedError('Entry type {} not yet implemented'.format(entry_type))

    return entry_dict
