# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ex_GUI2wwqTRX.ui'
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
        self.image = QLabel(self.centralwidget)
        self.image.setObjectName(u"image")
        self.image.setGeometry(QRect(170, 10, 51, 21))
        font = QFont()
        font.setPointSize(12)
        self.image.setFont(font)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 40, 341, 251))
        self.widget.setAutoFillBackground(True)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(120, 90, 101, 41))
        self.FRactalEyes = QLabel(self.centralwidget)
        self.FRactalEyes.setObjectName(u"FRactalEyes")
        self.FRactalEyes.setGeometry(QRect(320, 0, 151, 41))
        font1 = QFont()
        font1.setPointSize(15)
        self.FRactalEyes.setFont(font1)
        self.Feature1 = QTabWidget(self.centralwidget)
        self.Feature1.setObjectName(u"Feature1")
        self.Feature1.setGeometry(QRect(370, 40, 411, 401))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.widget_2 = QWidget(self.tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(30, 60, 351, 231))
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(80, 100, 201, 31))
        self.Feature1.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.widget_3 = QWidget(self.tab_2)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(30, 60, 351, 231))
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(80, 100, 201, 31))
        self.Feature1.addTab(self.tab_2, "")
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(80, 340, 201, 111))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(80, 310, 201, 21))
        font2 = QFont()
        font2.setPointSize(11)
        self.label.setFont(font2)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(570, 10, 151, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.Feature1.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.image.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"image will load here", None))
        self.FRactalEyes.setText(QCoreApplication.translate("MainWindow", u"Fractal Eyes v2.0", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Graph of data for specific Feature", None))
        self.Feature1.setTabText(self.Feature1.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Feature 1", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Graph of data for specific Feature", None))
        self.Feature1.setTabText(self.Feature1.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Feature 2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Table of Image Voxels labelled", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Save Data", None))
    # retranslateUi

