from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class WorkspaceTreeModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
        QStandardItemModel.__init__(self)

    @property
    def root_item(self):
        return self.invisibleRootItem()

    def add_item(self, name: str):
        item = QStandardItem(name)
        self.root_item.appendRow(item)

    def delete_items(self, indexes: QModelIndex):
        for i in indexes:
            self.removeRow(i.row())
