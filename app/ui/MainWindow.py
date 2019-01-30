from PyQt5.QtWidgets import QMainWindow, QApplication

from slide_viewer_47.common.slide_view_params import SlideViewParams
from slide_viewer_47.widgets.menu.slide_viewer_menu import SlideViewerMenu
from ui.MainWindow_ui import Ui_MainWindow
from ui.SlideViewerWidget import SlideViewerWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.slide_viewer_widget1 = SlideViewerWidget()
        self.slide_viewer_widget1.slide_viewer.load(SlideViewParams('/home/anton/Downloads/CMU-1.tiff'))

        self.slide_viewer_widget2 = SlideViewerWidget()
        self.slide_viewer_widget2.slide_viewer.load(SlideViewParams('/home/anton/Downloads/CMU-1.tiff'))

        self.tabWidget.addTab(self.slide_viewer_widget1, "Visualization")
        self.tabWidget.addTab(self.slide_viewer_widget2, "Analysis")

        slide_viewer_menu = SlideViewerMenu("actions", self.menuBar, self.slide_viewer_widget1.slide_viewer)
        self.menuBar.addMenu(slide_viewer_menu)

        self.actionExit.triggered.connect(lambda: QApplication.exit())
