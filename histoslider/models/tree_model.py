from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, pyqtSignal


class TreeModel(QAbstractItemModel):

    changed_showed = pyqtSignal(QModelIndex)

    def __init__(self, root_data, parent=None):
        super(TreeModel, self).__init__(parent)
        self._root = root_data

    def rowCount(self, index: QModelIndex):
        if index.isValid():
            return index.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, node, parent: QModelIndex = None):
        if not parent or not parent.isValid():
            parent = self._root
        else:
            parent = parent.internalPointer()
        parent.addChild(node)

    def removeRow(self, row: int, parent: QModelIndex = None):
        if not parent or not parent.isValid():
            # parent is not valid when it is the root node, since the "parent"
            # method returns an empty QModelIndex
            parentNode = self._root
        else:
            parentNode = parent.internalPointer()  # the node
        return parentNode.removeChild(row)

    def getItem(self, index: QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self._root

    def index(self, row, column, parent: QModelIndex = QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return self.createIndex(p.row(), 0, p)
        return QModelIndex()

    def columnCount(self, index: QModelIndex):
        if index.isValid():
            return index.internalPointer().columnCount()
        return self._root.columnCount()

    def data(self, index: QModelIndex, role):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            if index.column() != 2:
                return None
            item = self.getItem(index)
            return Qt.Checked if item.checked() else Qt.Unchecked

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        if index.column() == 2:
            return None

        item = self.getItem(index)
        return item.data(index.column())

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole:
            node = self.getItem(index)
            if node.set_checked(not node.checked()):
                self.changed_showed.emit(index)
                return True
        elif role == Qt.EditRole:
            item = self.getItem(index)
            result = item.setData(index.column(), value)

            if result:
                self.dataChanged.emit(index, index)

            return result
        else:
            return False

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return 0
        item = index.internalPointer()
        return item.flags(index.column())

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root.column_names[section]

        return None
