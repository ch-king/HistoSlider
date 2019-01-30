import os

from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from slide_viewer_47.common.slide_view_params import SlideViewParams
from ui.MainWindow_ui import Ui_MainWindow
from ui.SlideViewerWidget import SlideViewerWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # FOR TESTING PURPOSES!
        viewer = SlideViewerWidget()
        viewer.slide_viewer.load(SlideViewParams('/home/anton/Downloads/CMU-1.tiff'))
        self.tabWidget.addTab(viewer, os.path.basename('/home/anton/Downloads/CMU-1.tiff'))

        self.actionOpenFile.triggered.connect(self.load_slide)
        self.actionExit.triggered.connect(lambda: QApplication.exit())

        # slide_viewer_menu = SlideViewerMenu("actions", self.menuBar, self.slide_viewer_widget1.slide_viewer)
        # self.menuBar.addMenu(slide_viewer_menu)

    def load_slide(self):
        file_path = self.open_file_name_dialog()
        if file_path:
            # self.slide_viewer.load_slide(file_path, start_level=1, start_image_rect=QRectF(1000, 1000, 1000, 1000))
            viewer = SlideViewerWidget()
            viewer.slide_viewer.load(SlideViewParams(file_path))
            self.tabWidget.addTab(viewer, os.path.basename(file_path))
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
            "bif"]
        pillow_formats = [
            'bmp', 'bufr', 'cur', 'dcx', 'fits', 'fl', 'fpx', 'gbr',
            'gd', 'gif', 'grib', 'hdf5', 'ico', 'im', 'imt', 'iptc',
            'jpeg', 'jpg', 'jpe', 'mcidas', 'mic', 'mpeg', 'msp',
            'pcd', 'pcx', 'pixar', 'png', 'ppm', 'psd', 'sgi',
            'spider', 'tga', 'tiff', 'wal', 'wmf', 'xbm', 'xpm',
            'xv'
        ]
        available_formats = [*whole_slide_formats, *pillow_formats]
        available_extensions = ["." + available_format for available_format in available_formats]
        return available_extensions

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        file_ext_strings = ["*" + ext for ext in self.available_formats]
        file_ext_string = " ".join(file_ext_strings)
        file_name, _ = QFileDialog.getOpenFileName(self, "Select whole-slide image to view", "",
                                                   "Whole-slide images ({});;".format(file_ext_string),
                                                   options=options)
        return file_name
