from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog

from ui.ScreenshotDialog_ui import Ui_ScreenshotDialog


class ScreenshotDialog(QDialog, Ui_ScreenshotDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_size(self):
        return QSize(self.widthSpinBox.value(), self.heightSpinBox.value())

    def get_filepath(self):
        return self.pathLineEdit.text()
