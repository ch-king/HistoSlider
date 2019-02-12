from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, pyqtSignal

from histoslider.models.workspace_data import WorkspaceData


class WorkspaceModel(QAbstractItemModel):

    changed_showed = pyqtSignal(QModelIndex)

    def __init__(self, parent=None):
        super(WorkspaceModel, self).__init__(parent)
        self.workspace_data = WorkspaceData("Workspace")

    def rowCount(self, index: QModelIndex):
        if index.isValid():
            return index.internalPointer().childCount()
        return self.workspace_data.childCount()

    def addChild(self, node, parent: QModelIndex = None):
        if not parent or not parent.isValid():
            parent = self.workspace_data
        else:
            parent = parent.internalPointer()
        parent.addChild(node)

    def removeRow(self, row: int, parent: QModelIndex = None):
        if not parent or not parent.isValid():
            # parent is not valid when it is the root node, since the "parent"
            # method returns an empty QModelIndex
            parentNode = self.workspace_data
        else:
            parentNode = parent.internalPointer()  # the node
        return parentNode.removeChild(row)

    def getItem(self, index: QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.workspace_data

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
        return self.workspace_data.columnCount()

    def data(self, index: QModelIndex, role: int = None):
        if not index.isValid():
            return None

        item = self.getItem(index)

        if role == Qt.ToolTipRole:
            if index.column() == 0:
                return item.tooltip

        if role == Qt.DecorationRole:
            if index.column() == 0:
                return item.icon

        if role == Qt.CheckStateRole:
            if index.column() == 0:
                return Qt.Checked if item.checked else Qt.Unchecked

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() != 1:
                return item.data(index.column())

        return None

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        item = self.getItem(index)
        if role == Qt.CheckStateRole:
            item.checked = not item.checked
            self.changed_showed.emit(index)
            return True
        else:
            return False

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return 0
        item = index.internalPointer()
        return item.flags(index.column())

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.workspace_data.column_names[section]

        return None

    def load_workspace(self, path: str):
        with open(path, 'r') as file:
            self.workspace_data = WorkspaceData.from_json(file.read())
        self.workspace_data.path = path

    def save_workspace(self, path: str):
        self.workspace_data.path = path
        with open(path, 'w') as file:
            file.write(self.workspace_data.to_json())
