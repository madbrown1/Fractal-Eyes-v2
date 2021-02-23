# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore



import Functions as f

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui,self).__init__()
        uic.loadUi("Ex_GUI.ui", self)

        self.PatientBool = False
        self.saveBool = False
        self.fileSelected = False


        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button3 = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.button4 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')

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


    def Fractalize(self):
        self.rowSpin = self.findChild(QtWidgets.QSpinBox, 'spinBox')
        self.colSpin = self.findChild(QtWidgets.QSpinBox, 'spinBox_2')

        if self.PatientBool and self.saveBool and self.fileSelected and self.rowSpin.value() != 0 and self.colSpin.value() != 0:


            self.imgGrid = f.VoxelCreate(self.colSpin.value(),self.rowSpin.value(),self.ImagePath)
            #user decides voxel shape
            # if user selects rectangle
                #move on
            #if user selects 2 triangles
                #call tri 2 voxel
            #if user selects 4 triangles
            self.outVoxel = f.tri4Voxel(self.imgGrid, self.colSpin.value(),self.rowSpin.value())
            # Still waiting for circles
            #Move on to image classification
                #classification of image voxel through CNN

            ###FEATURE EXTRACTION
            self.labels = f.binary_thresholding(self.outVoxel)
            self.table = f.gain_regionprops(self.labels, self.outVoxel)
            self.saveTable, self.gvg = f.data_calculation(self.table) #include list of strings as argument for features, )
            f.data_organization(self.saveTable, self.gvg, self.saveDestination)
            #########################################################################################


            #image preprocessing functions
                #image resizing
                #image normalization
                #image voxel creation
            #Image Classification
                #Classification of Image Voxel
                #Trained CNN model
            #Feature Extraction
                #Extract Features
                #Determine Meta Data
            #output back through gui
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec()
