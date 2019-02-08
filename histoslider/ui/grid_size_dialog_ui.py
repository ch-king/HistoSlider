# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/anton/bblab/histoslider/histoslider/ui/grid_size_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GridSizeDialog(object):
    def setupUi(self, GridSizeDialog):
        GridSizeDialog.setObjectName("GridSizeDialog")
        GridSizeDialog.resize(190, 118)
        GridSizeDialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(GridSizeDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 80, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(GridSizeDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 171, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.widthLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.widthLabel.setObjectName("widthLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widthLabel)
        self.widthSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.widthSpinBox.setMaximum(32768)
        self.widthSpinBox.setProperty("value", 224)
        self.widthSpinBox.setObjectName("widthSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.widthSpinBox)
        self.heightLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.heightLabel.setObjectName("heightLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.heightLabel)
        self.heightSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.heightSpinBox.setMaximum(32768)
        self.heightSpinBox.setProperty("value", 224)
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.heightSpinBox)

        self.retranslateUi(GridSizeDialog)
        self.buttonBox.accepted.connect(GridSizeDialog.accept)
        self.buttonBox.rejected.connect(GridSizeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GridSizeDialog)

    def retranslateUi(self, GridSizeDialog):
        _translate = QtCore.QCoreApplication.translate
        GridSizeDialog.setWindowTitle(_translate("GridSizeDialog", "Grid Size"))
        self.widthLabel.setText(_translate("GridSizeDialog", "Width"))
        self.heightLabel.setText(_translate("GridSizeDialog", "Height"))

