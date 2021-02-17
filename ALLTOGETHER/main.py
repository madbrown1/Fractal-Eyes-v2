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


        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button3 = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.button4 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')





        self.button1.clicked.connect(self.ImportImage) #import Image
        self.button2.clicked.connect(lambda: f.test(self.button2.objectName())) #import patient data
        self.button3.clicked.connect(lambda: f.test(self.button3.objectName())) #import save patient data
        self.button4.clicked.connect(lambda: f.test(self.button4.objectName())) #FRACTALIZE EXTRACT

    def ImportImage(self):
        self.ImagePath, self.filter = QtWidgets.QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg *.png *.tif)")
        self.label3 = self.findChild(QtWidgets.QLabel, 'label_3')
        if self.ImagePath != "":
            pixmap = QtGui.QPixmap(self.ImagePath)

            self.label3.setGeometry(0, 0, self.frameGeometry().width()/2.2, self.frameGeometry().height()/2.2)
            self.label3.setScaledContents(True)

            self.label3.setPixmap(pixmap)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec()
