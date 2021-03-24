# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PIL import Image
import cv2
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import os


import Functions as f

class Ui(QtWidgets.QMainWindow):
    def __init__(self, Ui2):
        super(Ui,self).__init__()
        uic.loadUi("Ex_GUI.ui", self)
        self.featureStrings = []
        self.PatientBool = False
        self.saveBool = False
        self.fileSelected = False
        self.proceed = True
        self.outputWindow = Ui2
        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button3 = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.button4 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.radioCircle = self.findChild(QtWidgets.QRadioButton, 'radioButton')
        self.radioRect = self.findChild(QtWidgets.QRadioButton, 'radioButton_2')
        self.radio2tri = self.findChild(QtWidgets.QRadioButton, 'radioButton_3')
        self.radio4tri = self.findChild(QtWidgets.QRadioButton, 'radioButton_4')

        self.button1.clicked.connect(self.ImportImage) #import Image
        self.button2.clicked.connect(self.ImportPatientData) #import patient data
        self.button3.clicked.connect(self.SelectSave) #select save patient data
        self.button4.clicked.connect(self.Fractalize) #FRACTALIZE EXTRACT

    def ImportImage(self):
        self.ImagePath, self.filter = QtWidgets.QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg *.png *.tif)")
        self.label3 = self.findChild(QtWidgets.QLabel, 'label_3')
        if self.ImagePath != "":
            pixmap = QtGui.QPixmap(self.ImagePath)

            self.label3.setGeometry(0, 0, self.frameGeometry().width()/2.2, self.frameGeometry().height()/2.2)
            self.label3.setScaledContents(True)

            self.label3.setPixmap(pixmap)

        self.fileSelected = True


    def SelectSave(self):
        self.saveDestination = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(self.saveDestination)

        self.saveBool = True


    def ImportPatientData(self):
        self.patientData, self.filter = QtWidgets.QFileDialog.getOpenFileName(None, 'OpenFile', '',
                                                                            "Patient Data(*.txt *.dat)")
        self.PatientBool = True

    def collectFeatures(self):

        self.check1 = self.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.check2 = self.findChild(QtWidgets.QCheckBox, 'checkBox_2')
        self.check3 = self.findChild(QtWidgets.QCheckBox, 'checkBox_3')
        self.check4 = self.findChild(QtWidgets.QCheckBox, 'checkBox_4')

        self.check6 = self.findChild(QtWidgets.QCheckBox, 'checkBox_6')
        self.check7 = self.findChild(QtWidgets.QCheckBox, 'checkBox_7')

        if self.check1.isChecked():
            self.featureStrings.append('centroid')
        if self.check2.isChecked():
            self.featureStrings.append('avg_area')
        if self.check3.isChecked():
            self.featureStrings.append('avg_perimeter')
        if self.check4.isChecked():
            self.featureStrings.append('avg_eccentricity')
        if self.check6.isChecked():
            self.featureStrings.append('avg_major_axis_length')
        if self.check7.isChecked():
            self.featureStrings.append('avg_minor_axis_length')


    def Fractalize(self):
        self.rowSpin = self.findChild(QtWidgets.QSpinBox, 'spinBox')
        self.colSpin = self.findChild(QtWidgets.QSpinBox, 'spinBox_2')
        self.collectFeatures()


        if self.PatientBool and self.saveBool and self.fileSelected and self.rowSpin.value() != 0 and self.colSpin.value() != 0 and (
                self.radio4tri.isChecked() or self.radio2tri.isChecked() or self.radioRect.isChecked() or self.radioCircle.isChecked()):

            self.im = cv2.imread(self.ImagePath)
            self.imgGrid = f.VoxelCreate(self.colSpin.value(),self.rowSpin.value(), self.im)
            #user decides voxel shape


            if self.radio4tri.isChecked():
                self.outVoxel = f.tri4Voxel(self.imgGrid, self.colSpin.value(), self.rowSpin.value())
            elif self.radio2tri.isChecked():
                self.outVoxel = f.tri2UPVoxel(self.imgGrid, self.colSpin.value(), self.rowSpin.value())

            elif self.radioRect.isChecked():
                self.outVoxel = self.imgGrid
            elif self.radioCircle.isChecked():
                self.outVoxel = f.CircleVoxel(self.imgGrid, self.colSpin.value(), self.rowSpin.value())



            #Move on to image classification
                #classification of image voxel through CNN


            self.outputWindow.ImportImage(self.ImagePath)

            ###FEATURE EXTRACTION
            for n in range(0, self.rowSpin.value(),1):
                for m in range(0, self.colSpin.value(),1):
                    self.labels = f.binary_thresholding(self.outVoxel[n][m])
                    self.table = f.gain_regionprops(self.labels, self.outVoxel[n][m])
                    self.saveTable, self.gvg = f.data_calculation(self.table, self.featureStrings)
                    f.data_organization(self.saveTable, self.gvg, self.saveDestination,n,m)


            count = 0
            xVals = {}
            yVals = {}

            for feature in self.featureStrings:
                print(feature)
                self.outputWindow.AddTab(feature)

                for n in range(0, self.rowSpin.value(),1):
                    for m in range(0, self.colSpin.value(),1):
                        xVals[count] = str(n) + str(m)
                        yVals[count] = f.data_retrieve(n,m,self.saveDestination,feature)
                        count = count + 1

                self.outputWindow.SetGraph(xVals,yVals)

                count = 0


            #########################################################################################


        else:
            if not self.PatientBool:
                print("Forgot to select a patient")
            if not self.saveBool:
                print("Forgot to select a save destination")
            if not self.fileSelected:
                print("Forgot to load in an image")
            if self.rowSpin.value() == 0:
                print("Select a row value")
            if self.colSpin.value() == 0:
                print("Select a column value")
            if not (self.radio4tri.isChecked() or self.radio2tri.isChecked() or self.radioRect.isChecked() or self.radioCircle.isChecked()):
                print("Please select a voxel shape")

class Ui2(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui2,self).__init__()
        uic.loadUi("Ex_GUI2.ui", self)
        self.setWindowTitle("Output Window")

    def ImportImage(self, imagePath):
        self.ImagePath = imagePath
        self.label3 = self.findChild(QtWidgets.QLabel, 'label_3')

        if self.ImagePath != "":
            pixmap = QtGui.QPixmap(self.ImagePath)

            self.label3.setGeometry(0, 0, self.frameGeometry().width()/2.2, self.frameGeometry().height()/2.2)
            self.label3.setScaledContents(True)

            self.label3.setPixmap(pixmap)

    def AddTab(self, name):
        tab = QtWidgets.QWidget()
        tab.setObjectName(name)
        widget = QtWidgets.QWidget(tab)
        widget.setObjectName(name + '_graph')
        #widget.setGeometry(QtGui.QRect(30, 60, 351, 231))
        plotGraph = pg.PlotWidget(widget)


        self.Feature1.addTab(plotGraph, "")
        self.Feature1.setTabText(self.Feature1.indexOf(tab), name)

    def SetGraph(self, xVals, yVals):
        self.label_4.plot(xVals,yVals)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window2 = Ui2()
    window = Ui(window2)
    window2.show()
    window.show()
    app.exec()
