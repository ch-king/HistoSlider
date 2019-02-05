from PyQt5.QtWidgets import QDialog

from ui.GridSizeDialog_ui import Ui_GridSizeDialog


class GridSizeDialog(QDialog, Ui_GridSizeDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_size(self):
        return (self.widthSpinBox.value(), self.heightSpinBox.value())
