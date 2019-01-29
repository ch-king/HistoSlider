from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget

from slide_viewer_47.widgets.slide_viewer import SlideViewer
from slide_viewer_47.widgets.menu.slide_viewer_menu import SlideViewerMenu

from ui.MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.slide_viewer = SlideViewer(viewer_top_else_left=True)
        # self.setCentralWidget(self.slide_viewer)

        self.tabWidget.addTab(self.slide_viewer, "Visualization")
        self.tabWidget.addTab(QCalendarWidget(), "Analysis")

        slide_viewer_menu = SlideViewerMenu("actions", self.menuBar, self.slide_viewer)
        self.menuBar.addMenu(slide_viewer_menu)

        self.actionExit.triggered.connect(lambda: QApplication.exit())
