import uuid

import jsonpickle
from PyQt5.QtCore import Qt


class BaseData:

    column_flags = (Qt.ItemIsEnabled | Qt.ItemIsSelectable,
                Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable,
                Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

    column_names = ('Type', 'Name', 'Show')

    def __init__(self, name: str):
        self.id = uuid.uuid4().int
        self.name = name

        self._parent = None
        self._children = []
        self._row = 0
        self._checked = False

    @property
    def column_data(self):
        return (self.__class__.__name__, self.name, self._checked)

    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, json):
        return jsonpickle.decode(json)

    def columnCount(self):
        return len(self.column_names)

    def childCount(self):
        return len(self._children)

    def child(self, row: int):
        if 0 <= row < self.childCount():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)

    def removeChild(self, position: int):
        if position < 0 or position > self.childCount():
            return False
        child = self._children.pop(position)
        child._parent = None
        return True

    def data(self, column: int):
        if 0 <= column < self.columnCount():
            return self.column_data[column]

    def setData(self, column: int, value):
        column_name = self.column_names[column]
        if column_name == 'Name':
            self.name = str(value)
            return True
        elif column_name == 'Show':
            return self.set_checked(bool(value))
        return False

    def flags(self, column: int):
        return self.column_flags[column]

    def checked(self):
        return self._checked

    def set_checked(self, state: bool):
        self._checked = state
        return True
