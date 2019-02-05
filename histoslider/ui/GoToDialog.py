from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QDialog

from ui.GoToDialog_ui import Ui_GoToDialog


class GoToDialog(QDialog, Ui_GoToDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_rect(self):
        return QRectF(self.xSpinBox.value(), self.ySpinBox.value(), self.widthSpinBox.value(), self.heightSpinBox.value())

    def get_level(self):
        return self.levelSpinBox.value()
