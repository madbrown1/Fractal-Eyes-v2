# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ex_GUIefzdhe.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 50, 341, 251))
        self.widget.setAutoFillBackground(True)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(120, 90, 101, 41))
        self.FRactalEyes = QLabel(self.centralwidget)
        self.FRactalEyes.setObjectName(u"FRactalEyes")
        self.FRactalEyes.setGeometry(QRect(330, 0, 151, 41))
        font = QFont()
        font.setPointSize(15)
        self.FRactalEyes.setFont(font)
        self.image = QLabel(self.centralwidget)
        self.image.setObjectName(u"image")
        self.image.setGeometry(QRect(170, 20, 51, 21))
        font1 = QFont()
        font1.setPointSize(12)
        self.image.setFont(font1)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(500, 50, 161, 31))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(390, 90, 371, 211))
        font2 = QFont()
        font2.setPointSize(11)
        self.groupBox.setFont(font2)
        self.formLayoutWidget = QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 70, 181, 71))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(5, 5, 5, 5)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setPointSize(13)
        self.label.setFont(font3)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font3)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.spinBox = QSpinBox(self.formLayoutWidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setFont(font3)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spinBox)

        self.spinBox_2 = QSpinBox(self.formLayoutWidget)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setFont(font3)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinBox_2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 50, 91, 21))
        font4 = QFont()
        font4.setPointSize(11)
        font4.setBold(True)
        font4.setWeight(75)
        self.label_4.setFont(font4)
        self.verticalLayoutWidget = QWidget(self.groupBox)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(200, 50, 160, 141))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton_2 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout.addWidget(self.radioButton_2)

        self.radioButton = QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout.addWidget(self.radioButton)

        self.radioButton_3 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout.addWidget(self.radioButton_3)

        self.radioButton_4 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.verticalLayout.addWidget(self.radioButton_4)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(200, 30, 151, 21))
        font5 = QFont()
        font5.setPointSize(11)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setWeight(75)
        self.label_5.setFont(font5)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(390, 310, 361, 141))
        self.groupBox_2.setFont(font2)
        self.formLayoutWidget_2 = QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(40, 30, 281, 91))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.formLayout_2.setHorizontalSpacing(8)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.checkBox = QCheckBox(self.formLayoutWidget_2)
        self.checkBox.setObjectName(u"checkBox")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.checkBox)

        self.checkBox_6 = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.checkBox_6)

        self.checkBox_2 = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.checkBox_2)

        self.checkBox_7 = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.checkBox_7)

        self.checkBox_3 = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.formLayoutWidget_2)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.checkBox_4)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(60, 330, 121, 23))
        font6 = QFont()
        font6.setPointSize(9)
        self.pushButton_2.setFont(font6)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(200, 330, 121, 23))
        self.pushButton_3.setFont(font6)
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(60, 360, 261, 71))
        font7 = QFont()
        font7.setPointSize(16)
        font7.setBold(True)
        font7.setWeight(75)
        self.pushButton_4.setFont(font7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"image will load here", None))
        self.FRactalEyes.setText(QCoreApplication.translate("MainWindow", u"Fractal Eyes v2.0", None))
        self.image.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Import Image", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Grid Size and Voxel Shape", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"# of Rows", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"# of Columns", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Grid Size", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Rectangular", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Circular", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"Two Triangles", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"Four Triangles", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Image Voxel Shape", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Features to be Extracted", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Estimate Center", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"Major Axis Length", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Area", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"Minor Axis Length", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Perimeter", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"Eccentricity", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Import Patient Data", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Select Save Location", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Fractalize & Extract", None))
    # retranslateUi

