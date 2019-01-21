from PySide2.QtWidgets import QMainWindow, QApplication

from .MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.actionExit.triggered.connect(lambda: QApplication.exit())
