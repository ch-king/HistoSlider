from PyQt5.QtCore import QAbstractItemModel, Signal, Slot, QModelIndex, Qt, QRectF
from PyQt5.QtWidgets import QTreeView, QMenu, QAction

from imcslider.Roi import RoiCircle
from models.data_classes import RootData, data_parser, AlignPointsContainer, AlignPoints
from utils.helpers import save_json, load_json

__author__ = 'vitoz'


class SlidesTreeView(QTreeView):
    def selectionChanged(self, new, old):
        super().selectionChanged(new, old)

    def openTreeContextMenu(self, position):
        idx = self.indexAt(position)
        obj = self.model().getItem(idx)

        menu = QMenu()
        if obj.data_type != 'align_points_container':
            add_apc = QAction(self)
            add_apc.setText('Add align point container')
            add_apc.triggered.connect(lambda: self.model().add_align_points_container(parent_idx=idx))
            menu.addAction(add_apc)

        menu.exec_(self.viewport().mapToGlobal(position))


class TreeModel(QAbstractItemModel):
    changed_showed = Signal(QModelIndex)

    def __init__(self, data_list, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = None
        self.entry_dict = self.setupModelData(data_list)
        # test
        self.changed_showed.connect(self.test)

    def setupModelData(self, data_list):
        if self.rootItem is None:
            self.rootItem = RootData()

        entry_dict = data_parser(data_list, self.rootItem)
        return entry_dict

    def columnCount(self, parent=QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            if index.column() != 2:
                return None
            item = self.getItem(index)
            if item.checked():
                return Qt.Checked
            else:
                return Qt.Unchecked

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0
        item = index.internalPointer()
        return item.flags(index.column())

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.column_names[section]

        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                                            self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
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

    @Slot(QModelIndex)
    def test(self, idx):
        item = self.getItem(idx)
        print(item.checked())

    # def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
    #     if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
    #         return False
    #
    #     result = self.rootItem.setData(section, value)
    #     if result:
    #         self.headerDataChanged.emit(orientation, section, section)
    #
    #     return result

    def add_align_points_container(self, parent_idx):
        self.layoutAboutToBeChanged.emit()
        # create container
        parent_item = self.getItem(parent_idx)
        align_point_container = AlignPointsContainer(name='Align points container',
                                                     parent_ids=[parent_item.id],
                                                     entry_dict=self.entry_dict)

        self.layoutChanged.emit()
        return align_point_container

    def add_align_point(self, parent_idx, position, graph_item, view):
        parent = self.getItem(parent_idx)
        if parent.data_type != 'align_points_container':
            if parent.parents[0].data_type == 'align_points_container':
                parent = parent.parents[0]
            else:
                parent = self.add_align_points_container(parent_idx)

        AlignPoints(position, parent_ids=[parent.id], entry_dict=parent.entry_dict)
        self.layoutChanged.emit()
        pos = graph_item.mapFromScene(view.mapToScene(position))
        size = 1000
        ap = RoiCircle(QRectF(pos.x() - size / 2, pos.y() - size / 2, size, size), parent=graph_item, view=view)

    def save_as_file(self, filename):
        try:
            save_json(self.entry_dict, filename)
            return True
        except:
            return False

    def read_file(self, filename):
        try:
            dat_list = load_json(filename)
        except:
            return False
        self.layoutAboutToBeChanged.emit()
        self.beginResetModel()
        self.rootItem = None
        self.entry_dict = self.setupModelData(dat_list)
        self.layoutChanged.emit()
        self.endResetModel()
