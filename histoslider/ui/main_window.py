import os
from functools import partial

import psutil
from PyQt5.QtCore import Qt, QTimer, QModelIndex, QSettings, QByteArray, QItemSelection
from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QLabel,
    QApplication,
    QMenu,
    QAction, QDialog)
from pyqtgraph import HistogramLUTWidget

from histoslider.core.decorators import catch_error
from histoslider.core.message import TreeViewCurrentItemChangedMessage, SlideRemovedMessage, SlideImportedMessage
from histoslider.image.mcd_loader import McdLoader
from histoslider.image.slide_view import SlideView
from histoslider.image.tiff_loader import TiffLoader
from histoslider.models.data_manager import DataManager
from histoslider.ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self, report_error_callback):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.report_error = report_error_callback

        self.process = psutil.Process(os.getpid())
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.update_memory_usage)
        self.ui_timer.start(1000)

        self.memory_usage_label = QLabel()
        self.statusBar.addPermanentWidget(self.memory_usage_label)

        self.treeViewOverview.setModel(DataManager.workspace_model)
        self.treeViewOverview.customContextMenuRequested.connect(self.open_menu)
        self.treeViewOverview.selectionModel().selectionChanged.connect(self._treeview_selection_changed)
        self.treeViewOverview.selectionModel().currentChanged.connect(self._treeview_current_changed)

        self.histogram = HistogramLUTWidget(self)
        self.viewer = SlideView(self, self.histogram)
        self.verticalLayoutSettings.addWidget(self.histogram)

        self.tabWidget.addTab(self.viewer, "Blend")

        self.actionImportSlide.triggered.connect(self.import_slide_dialog)
        self.actionOpenWorkspace.triggered.connect(self.load_workspace_dialog)
        self.actionSaveWorkspace.triggered.connect(self.save_workspace_dialog)
        self.actionExit.triggered.connect(lambda: QApplication.exit())

        self.load_settings()

    def _treeview_current_changed(self, current: QModelIndex, previous: QModelIndex):
        if current.isValid():
            item = current.model().getItem(current)
            DataManager.hub.broadcast(TreeViewCurrentItemChangedMessage(self, item))

    def _treeview_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()

    def load_settings(self):
        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QByteArray()))

    def save_settings(self):
        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())

    def load_workspace_dialog(self):
        options = QFileDialog.Options()
        file_ext = "*.json"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Workspace",
            "",
            "Workspace Files ({})".format(file_ext),
            options=options,
        )
        if file_path:
            DataManager.load_workspace(file_path)

    def save_workspace_dialog(self):
        file_ext = "*.json"
        dialog = QFileDialog(self)
        dialog.setDefaultSuffix(".json")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setWindowTitle("Save Workspace")
        dialog.setNameFilter("Workspace Files ({})".format(file_ext))
        if dialog.exec() == QDialog.Accepted:
            DataManager.save_workspace(dialog.selectedFiles()[0])

    def open_menu(self, position):
        indexes = self.treeViewOverview.selectedIndexes()

        level = None
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu(self.treeViewOverview)

        if level == 1:
            action = QAction("Delete slide", menu)
            action.triggered.connect(partial(self.delete_slide, indexes))
            menu.addAction(action)
        elif level == 2:
            menu.addAction("Edit object/container")
        elif level == 3:
            menu.addAction("Edit object")

        menu.exec_(self.treeViewOverview.viewport().mapToGlobal(position))

    def update_memory_usage(self):
        # return the memory usage in MB
        mem = self.process.memory_info()[0] / float(2 ** 20)
        self.memory_usage_label.setText(f"Memory usage: {mem:.2f} Mb")

    @catch_error("Could not import slide")
    def import_slide(self, file_path: str):
        filename, file_extension = os.path.splitext(file_path)
        if file_extension == '.mcd':
            loader = McdLoader(file_path)
            slide = loader.load()
        elif file_extension == '.tiff' or file_extension == '.tif':
            loader = TiffLoader(file_path)
            slide = loader.load()
        else:
            loader = TiffLoader(file_path)
            slide = loader.load()
        DataManager.workspace_model.beginResetModel()
        DataManager.workspace_model.workspace_data.add_slide(slide)
        DataManager.workspace_model.endResetModel()
        QPixmapCache.clear()
        DataManager.hub.broadcast(SlideImportedMessage(self))

    def delete_slide(self, indexes: [QModelIndex]):
        DataManager.workspace_model.beginResetModel()
        for index in indexes:
            DataManager.workspace_model.removeRow(index.row(), parent=index.parent())
        DataManager.workspace_model.endResetModel()
        QPixmapCache.clear()
        DataManager.hub.broadcast(SlideRemovedMessage(self))

    def import_slide_dialog(self):
        options = QFileDialog.Options()
        file_ext_strings = ["*.mcd", "*.tiff", "*.tif"]
        file_ext_string = " ".join(file_ext_strings)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select whole-slide image to view",
            "",
            "Whole-slide images ({});;".format(file_ext_string),
            options=options,
        )
        if file_path:
            self.import_slide(file_path)

    @property
    def okToQuit(self):
        return True

    def closeEvent(self, event):
        if self.okToQuit:
            self.save_settings()
