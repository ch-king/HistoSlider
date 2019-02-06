class TreeNode:
    def __init__(self, data):
        self._data = data

        self._columncount = len(self._data)
        self._children = []
        self._parent = None
        self._row = 0

        self.media = None
        self.query = None

    def data(self, in_column):
        if in_column >= 0 and in_column < len(self._data):
            return self._data[in_column]

    def columnCount(self):
        return self._columncount

    def childCount(self):
        return len(self._children)

    def child(self, in_row):
        if in_row >= 0 and in_row < self.childCount():
            return self._children[in_row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def childCount(self):
        return len(self._children)

    def addChild(self, in_child):
        in_child._parent = self
        in_child._row = len(self._children)
        self._children.append(in_child)
        self._columncount = max(in_child.columnCount(), self._columncount)

    def setMedia(self, media):
        self.media = media
