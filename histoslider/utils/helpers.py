import json

from PIL import Image


def default_value(val, default, sentinel=None):
    """
    Returns a default value if the value is equal to the sentinel
    :param val: a value
    :param default: a value
    :param sentinel: a sentinel value
    :return: val or default val

    >>> default_value(None, 1)
    1
    >>> default_value(2, 1)
    2
    >>> default_value(2, 1, sentinel=2)
    1
    """
    return default if val is sentinel else val


class IdBasedProperty(property):
    """
    A custom property which returns values based on ids defined in the id_varname and a dictionary dict_name.
    Supports also setting of the property and deleting.
    Assumes that all the object in the dict have an id attribute
    """

    def __init__(self, id_varname: str, dict_name: str):
        def fget(obj):
            var_list = list()
            obj_dict = getattr(obj, dict_name)
            for id in getattr(obj, id_varname):
                par = obj_dict.get(id)
                if par is not None:
                    var_list.append(par)
            return var_list

        def fset(obj, values):
            var_list = list()
            for val in values:
                var_list.append(val.id)
            setattr(obj, id_varname, var_list)

        def fdel(obj):
            setattr(obj, id_varname, set())

        super().__init__(fget, fset, fdel)

def save_json(entry_dict, filename):
    dlist = _data_tolist(entry_dict)
    _dump_json(dlist, filename)

def load_json(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    return data


def _data_tolist(entry_dict):
    dumps =list()
    for key, entry in entry_dict.items():
        d = entry.dump()
        if d is not None:
            dumps.append(entry.dump())
    return dumps

def _dump_json(obj, file_name):
    with open(file_name, 'w') as outfile:
        json.dump(obj, outfile, sort_keys=True,
                 indent=4,separators=(',', ': '))

def dummyImageDecorator(func):
    """
    Decorates the function that is supposed to return an image, such that
    it does only return an emtpy image if self.img is None

    :param func: The function
    :return: the function or an empty image
    """

    def func_wrapper(*args, **kwargs):
        if args[0].img is not None:
            return func(*args, **kwargs)
        else:
            size = kwargs.get('size', (100, 100))
            return Image.new('RGBA', size)

    return func_wrapper
