import os
from functools import partial

import psutil
from PyQt5.QtCore import Qt, QTimer, QModelIndex, QSettings, QByteArray
from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QLabel,
    QApplication,
    QMenu,
    QAction, QDialog, QWidget, QAbstractItemView)

from histoslider.models.data_manager import DataManager
from histoslider.models.slide_data import SlideData
from histoslider.openslide_viewer.common.slide_view_params import SlideViewParams
from histoslider.ui.main_window_ui import Ui_MainWindow
from histoslider.ui.slide_viewer_widget import SlideViewerWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.process = psutil.Process(os.getpid())
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.update_memory_usage)
        self.ui_timer.start(1000)

        self.memory_usage_label = QLabel()
        self.statusBar.addPermanentWidget(self.memory_usage_label)

        self.treeViewOverview.setModel(DataManager.tree_model)
        self.treeViewOverview.customContextMenuRequested.connect(self.open_menu)
        self.treeViewOverview.setSelectionBehavior(QAbstractItemView.SelectItems)

        self.actionOpenSlide.triggered.connect(self.load_slide_dialog)
        self.actionOpenWorkspace.triggered.connect(self.load_workspace_dialog)
        self.actionSaveWorkspace.triggered.connect(self.save_workspace_dialog)
        self.actionExit.triggered.connect(lambda: QApplication.exit())

        self.load_settings()

        # FOR TESTING PURPOSES!
        self.load_slide("/home/anton/Pictures/CMU-1.tiff")

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
            "Load HistoSlider Workspace",
            "",
            "Workspace Files ({})".format(file_ext),
            options=options,
        )
        if file_path:
            DataManager.load_workspace(file_path)
            self.treeViewOverview.setModel(DataManager.tree_model)

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

    def load_slide(self, file_path):
        viewer = SlideViewerWidget()
        file_name = os.path.basename(file_path)
        tab_index = self.tabWidget.addTab(viewer, file_name)
        DataManager.tree_model.beginResetModel()
        DataManager.workspace.addChild(SlideData(file_name, tab_index))
        DataManager.tree_model.endResetModel()
        viewer.slide_viewer.load(SlideViewParams(file_path))
        QPixmapCache.clear()

    def delete_slide(self, indexes: [QModelIndex]):
        for index in indexes:
            DataManager.tree_model.beginRemoveRows(index.parent(), index.row(), index.row())
            item = DataManager.tree_model.getItem(index)
            self.tabWidget.removeTab(item.tab_index)
            success = DataManager.tree_model.removeRow(index.row(), parent=index.parent())
            DataManager.tree_model.endRemoveRows()
        QPixmapCache.clear()

    @property
    def available_formats(self):
        whole_slide_formats = [
            "svs",
            "vms",
            "vmu",
            "ndpi",
            "scn",
            "mrx",
            "tiff",
            "svslide",
            "tif",
            "bif",
            "mrxs",
            "bif",
        ]
        pillow_formats = [
            "bmp",
            "bufr",
            "cur",
            "dcx",
            "fits",
            "fl",
            "fpx",
            "gbr",
            "gd",
            "gif",
            "grib",
            "hdf5",
            "ico",
            "im",
            "imt",
            "iptc",
            "jpeg",
            "jpg",
            "jpe",
            "mcidas",
            "mic",
            "mpeg",
            "msp",
            "pcd",
            "pcx",
            "pixar",
            "png",
            "ppm",
            "psd",
            "sgi",
            "spider",
            "tga",
            "tiff",
            "wal",
            "wmf",
            "xbm",
            "xpm",
            "xv",
        ]
        available_formats = [*whole_slide_formats, *pillow_formats]
        available_extensions = [
            "." + available_format for available_format in available_formats
        ]
        return available_extensions

    def load_slide_dialog(self):
        options = QFileDialog.Options()
        file_ext_strings = ["*" + ext for ext in self.available_formats]
        file_ext_string = " ".join(file_ext_strings)
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select whole-slide image to view",
            "",
            "Whole-slide images ({});;".format(file_ext_string),
            options=options,
        )
        if file_path:
            self.load_slide(file_path)

    @property
    def okToContinue(self):
        return True

    def closeEvent(self, event):
        if self.okToContinue:
            self.save_settings()
