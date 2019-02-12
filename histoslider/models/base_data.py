import uuid

from PyQt5.QtCore import Qt


class BaseData:
    column_names = ['Name']
    column_flags = [Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable]

    def __init__(self, name: str):
        self.id = uuid.uuid4().int
        self.name = name

        self._parent = None
        self._children = []
        self._row = 0
        self._checked = False

    @property
    def icon(self):
        return None

    @property
    def tooltip(self):
        return None

    @property
    def column_data(self):
        return [self.name]

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
        if column == 0:
            self.checked = value
            return True
        return False

    def flags(self, column: int):
        return self.column_flags[column]

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, state: bool):
        self._checked = bool(state)
