# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/anton/bblab/histoslider/histoslider/ui/go_to_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GoToDialog(object):
    def setupUi(self, GoToDialog):
        GoToDialog.setObjectName("GoToDialog")
        GoToDialog.resize(190, 218)
        GoToDialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(GoToDialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 180, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(GoToDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 171, 161))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.levelLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.levelLabel.setObjectName("levelLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.levelLabel)
        self.levelSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.levelSpinBox.setProperty("value", 1)
        self.levelSpinBox.setObjectName("levelSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.levelSpinBox)
        self.xLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.xLabel.setObjectName("xLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.xLabel)
        self.xSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.xSpinBox.setMaximum(32768)
        self.xSpinBox.setProperty("value", 1000)
        self.xSpinBox.setObjectName("xSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.xSpinBox)
        self.yLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.yLabel.setObjectName("yLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.yLabel)
        self.ySpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.ySpinBox.setMaximum(32768)
        self.ySpinBox.setProperty("value", 1000)
        self.ySpinBox.setObjectName("ySpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ySpinBox)
        self.widthLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.widthLabel.setObjectName("widthLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.widthLabel)
        self.widthSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.widthSpinBox.setMaximum(32768)
        self.widthSpinBox.setProperty("value", 1000)
        self.widthSpinBox.setObjectName("widthSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.widthSpinBox)
        self.heightLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.heightLabel.setObjectName("heightLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.heightLabel)
        self.heightSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.heightSpinBox.setMaximum(32768)
        self.heightSpinBox.setProperty("value", 1000)
        self.heightSpinBox.setObjectName("heightSpinBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.heightSpinBox)

        self.retranslateUi(GoToDialog)
        self.buttonBox.accepted.connect(GoToDialog.accept)
        self.buttonBox.rejected.connect(GoToDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GoToDialog)

    def retranslateUi(self, GoToDialog):
        _translate = QtCore.QCoreApplication.translate
        GoToDialog.setWindowTitle(_translate("GoToDialog", "Go To"))
        self.levelLabel.setText(_translate("GoToDialog", "Level"))
        self.xLabel.setText(_translate("GoToDialog", "X"))
        self.yLabel.setText(_translate("GoToDialog", "Y"))
        self.widthLabel.setText(_translate("GoToDialog", "Width"))
        self.heightLabel.setText(_translate("GoToDialog", "Height"))

