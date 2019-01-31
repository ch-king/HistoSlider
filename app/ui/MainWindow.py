import os
from functools import partial

import psutil
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QModelIndex
from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QLabel,
    QApplication,
    QMenu,
    QAction,
)

from models.slide_list_model import SlideListModel
from slide_viewer_47.common.slide_view_params import SlideViewParams
from ui.MainWindow_ui import Ui_MainWindow
from ui.SlideViewerWidget import SlideViewerWidget


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

        self.slide_list = SlideListModel()
        self.treeViewSlides.setModel(self.slide_list)
        self.treeViewSlides.customContextMenuRequested.connect(self.open_menu)

        self.actionOpenFile.triggered.connect(self.open_load_slide_dialog)
        self.actionExit.triggered.connect(lambda: QApplication.exit())

        # FOR TESTING PURPOSES!
        self.load_slide("/home/anton/Downloads/CMU-1.tiff")

    def open_menu(self, position):
        indexes = self.treeViewSlides.selectedIndexes()

        level = None
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu(self.treeViewSlides)

        if level == 0:
            action = QAction("Delete slide", menu)
            action.triggered.connect(partial(self.delete_slide, indexes))
            menu.addAction(action)
        elif level == 1:
            menu.addAction("Edit object/container")
        elif level == 2:
            menu.addAction("Edit object")

        menu.exec_(self.treeViewSlides.viewport().mapToGlobal(position))

    def delete_slide(self, indexes: [QModelIndex]):
        self.slide_list.delete_items(indexes)

    def update_memory_usage(self):
        # return the memory usage in MB
        mem = self.process.memory_info()[0] / float(2 ** 20)
        self.memory_usage_label.setText(f"Memory usage: {mem:.2f} Mb")

    def load_slide(self, file_path):
        viewer = SlideViewerWidget()
        viewer.slide_viewer.load(SlideViewParams(file_path))
        file_name = os.path.basename(file_path)
        self.tabWidget.addTab(viewer, file_name)
        self.slide_list.add_item(file_name)
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

    def open_load_slide_dialog(self):
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
