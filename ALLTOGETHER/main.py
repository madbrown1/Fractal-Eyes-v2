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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

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
        self.check1 = self.findChild(QtWidgets.QCheckBox, 'checkBox')
        self.check1.setText("Shading")
        self.button1.clicked.connect(self.ImportImage) #import Image
        self.button2.clicked.connect(self.ImportPatientData) #import patient data
        self.button3.clicked.connect(self.SelectSave) #select save patient data
        self.button4.clicked.connect(self.Fractalize) #FRACTALIZE EXTRACT
        self.outputWindow.pushButton.clicked.connect(self.outputWindow.saveData)


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
            self.featureStrings.append('shading')
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

            self.outputWindow.ImportImage(self.ImagePath)
            self.popupwindow = Popup(self, self.rowSpin.value(), self.colSpin.value())


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
            if not (
                    self.radio4tri.isChecked() or self.radio2tri.isChecked() or self.radioRect.isChecked() or self.radioCircle.isChecked()):
                print("Please select a voxel shape")


    def FeatureExtractionAll(self):
        self.popupwindow.close()
        for n in range(0, self.rowSpin.value(),1):
            for m in range(0, self.colSpin.value(),1):
                self.labels = f.binary_thresholding(self.outVoxel[n][m])
                self.table = f.gain_regionprops(self.labels, self.outVoxel[n][m])
                self.saveTable, self.gvg = f.data_calculation(self.table, self.featureStrings)
                f.data_organization(self.saveTable, self.gvg, self.saveDestination,n,m)
      
        count = 0
        xVals = {}
        self.yVals = {}
        graphNum = 1
        for feature in self.featureStrings:
            print(feature)
            #self.outputWindow.AddTab(feature)

            for n in range(0, self.rowSpin.value(),1):
                for m in range(0, self.colSpin.value(),1):
                    xVals[count] = str(n) + str(m)
                    self.yVals[count] = f.data_retrieve(n, m, self.saveDestination, feature)
                    count = count + 1

            self.outputWindow.SetGraph(xVals, self.yVals, feature,graphNum)
            self.outputWindow.SetVals(self.rowSpin.value(), self.colSpin.value(), self.yVals, self.saveDestination)
            graphNum = graphNum + 1

            count = 0
        self.outputWindow.activateWindow()


    def FeatureExtractionSpecific(self,n,m):


        self.popupwindow.close()
        self.labels = f.binary_thresholding(self.outVoxel[n][m])
        self.table = f.gain_regionprops(self.labels, self.outVoxel[n][m])
        self.saveTable, self.gvg = f.data_calculation(self.table, self.featureStrings)
        f.data_organization(self.saveTable, self.gvg, self.saveDestination,n,m)


        count = 0
        xVals = {}
        self.yVals = {}
        graphNum = 1
        for feature in self.featureStrings:
            print(feature)
            #self.outputWindow.AddTab(feature)


            xVals[count] = str(n) + str(m)
            self.yVals[count] = f.data_retrieve(n, m, self.saveDestination,feature)
            count = count + 1

            self.outputWindow.SetGraph(xVals, self.yVals, feature,graphNum)
            self.outputWindow.SetVals(self.rowSpin.value(), self.colSpin.value(), self.yVals, self.saveDestination)
            graphNum = graphNum + 1

            count = 0
        self.outputWindow.activateWindow()


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



    def SetGraph(self, xVals, yVals, plotTitle, graphNum):
        if graphNum == 1:
            figure = plt.figure()
            canvas = FigureCanvas(figure)
            layout = QtWidgets.QGridLayout()
            self.tab.setLayout(layout)
            layout.addWidget(canvas)



            ax = figure.add_subplot(111)
            ax.scatter(xVals.values(), yVals.values())
            ax.set(title = plotTitle, xlabel = 'Voxel Designation', ylabel = 'Value (in px)')


            xNames = list(xVals.values())
            yNames = list(yVals.values())
            yNames = [round(num,2) for num in yNames]

            for i, txt in enumerate(yVals.values()):
                ax.annotate(round(txt,2), (xNames[i], yNames[i]))
            plt.tight_layout(pad=4)


            canvas.draw()


        elif graphNum ==2:
            figure = plt.figure()
            canvas = FigureCanvas(figure)
            layout = QtWidgets.QGridLayout()
            self.tab_2.setLayout(layout)
            layout.addWidget(canvas)
            ax = figure.add_subplot(111)
            ax.scatter(xVals.values(), yVals.values())
            ax.set(title=plotTitle, xlabel='Voxel Designation', ylabel='Value (in px)')

            xNames = list(xVals.values())
            yNames = list(yVals.values())
            yNames = [round(num, 2) for num in yNames]

            for i, txt in enumerate(yVals.values()):
                ax.annotate(round(txt, 2), (xNames[i], yNames[i]))
            plt.tight_layout(pad=4)

            canvas.draw()

        else:
            tab = QtWidgets.QWidget()
            self.Feature1.addTab(tab, "Feature" + str(graphNum))
            figure = plt.figure()
            canvas = FigureCanvas(figure)
            layout = QtWidgets.QGridLayout()
            tab.setLayout(layout)
            layout.addWidget(canvas)

            ax = figure.add_subplot(111)
            ax.scatter(xVals.values(), yVals.values())
            ax.set(title=plotTitle, xlabel='Voxel Designation', ylabel='Value (in px)')

            xNames = list(xVals.values())
            yNames = list(yVals.values())
            yNames = [round(num, 2) for num in yNames]

            for i, txt in enumerate(yVals.values()):
                ax.annotate(round(txt, 2), (xNames[i], yNames[i]))
            plt.tight_layout(pad=4)

            canvas.draw()


    def SetVals(self, rowSpin, colSpin, Vals, saveDestination):
        self.rowSpin = rowSpin
        self.colSpin = colSpin
        self.Vals = Vals
        self.saveDestination = saveDestination
       

    def saveData(self):


        for n in range(0, self.rowSpin, 1):
            for m in range(0, self.colSpin, 1):
               f.save_data(n,m,self.saveDestination)



class Popup(QtGui.QMainWindow):
    def __init__(self, mainWindow, maxN, maxM):
        super(Popup, self).__init__()
        self.setGeometry(50,50,300,100)
        self.setWindowTitle("Select Individual or All Voxels")
        self.mainWindow = mainWindow
        self.maxN = maxN
        self.maxM = maxM

        vLayout = QtWidgets.QVBoxLayout()
        hLayout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setText("Select which voxels for processing:")
        label2 = QtWidgets.QLabel()
        label2.setText("OR")

        self.rowCombo = QtWidgets.QComboBox()
        self.colCombo = QtWidgets.QComboBox()

        rowRange = [str(x).zfill(1) for x in range(maxN)]
        colRange = [str(x).zfill(1) for x in range(maxM)]

        self.rowCombo.addItems(rowRange)
        self.colCombo.addItems(colRange)


        self.rowCombo.setAccessibleName("Row Index")
        self.colCombo.setAccessibleName("Col Index")

        allVoxelsButton = QtWidgets.QPushButton()
        allVoxelsButton.setText("All Voxels")
        specificVoxelButton = QtWidgets.QPushButton()
        specificVoxelButton.setText("Specific Voxel")
        vlayout2 = QtWidgets.QVBoxLayout()

        label3 = QtWidgets.QLabel()
        label3.setText("Row Voxel Index")
        label4 = QtWidgets.QLabel()
        label4.setText("Col Voxel Index")

        hLayout2 = QtWidgets.QHBoxLayout()
        hLayout3 = QtWidgets.QHBoxLayout()

        hLayout2.addWidget(label3)
        hLayout2.addWidget(self.rowCombo)
        hLayout3.addWidget(label4)
        hLayout3.addWidget(self.colCombo)

        vlayout2.addLayout(hLayout2)
        vlayout2.addLayout(hLayout3)
        vlayout2.addWidget(specificVoxelButton)
        hLayout.addWidget(allVoxelsButton, 1)
        hLayout.addWidget(label2,2)



        hLayout.addLayout(vlayout2,3)


        vLayout.addWidget(label, 1)
        vLayout.addLayout(hLayout, 2)

        widget = QtWidgets.QWidget()
        widget.setLayout(vLayout)

        allVoxelsButton.clicked.connect(self.mainWindow.FeatureExtractionAll)
        specificVoxelButton.clicked.connect(self.SpecificVoxel)


        self.setCentralWidget(widget)
        self.show()
        self.activateWindow()
    def SpecificVoxel(self):

        self.rowComboVal = int(self.rowCombo.currentText())
        self.colComboVal = int(self.colCombo.currentText())
        self.mainWindow.FeatureExtractionSpecific(self.rowComboVal, self.colComboVal)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window2 = Ui2()
    window = Ui(window2)
    window2.show()
    window.show()
    app.exec()
