# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/anton/bblab/histoslider/histoslider/ui/slide_info_widget.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SlideInfoWidget(object):
    def setupUi(self, SlideInfoWidget):
        SlideInfoWidget.setObjectName("SlideInfoWidget")
        SlideInfoWidget.resize(385, 127)
        self.verticalLayout = QtWidgets.QVBoxLayout(SlideInfoWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.levelDownsampleLabel = QtWidgets.QLabel(SlideInfoWidget)
        self.levelDownsampleLabel.setObjectName("levelDownsampleLabel")
        self.verticalLayout.addWidget(self.levelDownsampleLabel)
        self.levelSizeLabel = QtWidgets.QLabel(SlideInfoWidget)
        self.levelSizeLabel.setObjectName("levelSizeLabel")
        self.verticalLayout.addWidget(self.levelSizeLabel)
        self.mouseSceneLabel = QtWidgets.QLabel(SlideInfoWidget)
        self.mouseSceneLabel.setObjectName("mouseSceneLabel")
        self.verticalLayout.addWidget(self.mouseSceneLabel)
        self.viewSceneLabel = QtWidgets.QLabel(SlideInfoWidget)
        self.viewSceneLabel.setObjectName("viewSceneLabel")
        self.verticalLayout.addWidget(self.viewSceneLabel)
        self.selectedAreaLabel = QtWidgets.QLabel(SlideInfoWidget)
        self.selectedAreaLabel.setObjectName("selectedAreaLabel")
        self.verticalLayout.addWidget(self.selectedAreaLabel)

        self.retranslateUi(SlideInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(SlideInfoWidget)

    def retranslateUi(self, SlideInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        SlideInfoWidget.setWindowTitle(_translate("SlideInfoWidget", "Slide Info"))
        self.levelDownsampleLabel.setText(_translate("SlideInfoWidget", "Level, Downsample:"))
        self.levelSizeLabel.setText(_translate("SlideInfoWidget", "Level Size:"))
        self.mouseSceneLabel.setText(_translate("SlideInfoWidget", "Mouse Scene:"))
        self.viewSceneLabel.setText(_translate("SlideInfoWidget", "View Scene:"))
        self.selectedAreaLabel.setText(_translate("SlideInfoWidget", "Selected Area (0-level):"))


