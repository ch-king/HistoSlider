# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/anton/bblab/histoslider/histoslider/ui/screenshot_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ScreenshotDialog(object):
    def setupUi(self, ScreenshotDialog):
        ScreenshotDialog.setObjectName("ScreenshotDialog")
        ScreenshotDialog.resize(291, 149)
        ScreenshotDialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(ScreenshotDialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 110, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(ScreenshotDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 91))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.widthLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.widthLabel.setObjectName("widthLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widthLabel)
        self.widthSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.widthSpinBox.setMaximum(32768)
        self.widthSpinBox.setProperty("value", 1000)
        self.widthSpinBox.setObjectName("widthSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.widthSpinBox)
        self.heightLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.heightLabel.setObjectName("heightLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.heightLabel)
        self.heightSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.heightSpinBox.setMaximum(32768)
        self.heightSpinBox.setProperty("value", 1000)
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.heightSpinBox)
        self.pathLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.pathLabel.setObjectName("pathLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pathLabel)
        self.pathLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pathLineEdit)

        self.retranslateUi(ScreenshotDialog)
        self.buttonBox.accepted.connect(ScreenshotDialog.accept)
        self.buttonBox.rejected.connect(ScreenshotDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ScreenshotDialog)

    def retranslateUi(self, ScreenshotDialog):
        _translate = QtCore.QCoreApplication.translate
        ScreenshotDialog.setWindowTitle(_translate("ScreenshotDialog", "Take Screenshot"))
        self.widthLabel.setText(_translate("ScreenshotDialog", "Width"))
        self.heightLabel.setText(_translate("ScreenshotDialog", "Height"))
        self.pathLabel.setText(_translate("ScreenshotDialog", "Path"))
        self.pathLineEdit.setText(_translate("ScreenshotDialog", "screenshot.jpg"))

