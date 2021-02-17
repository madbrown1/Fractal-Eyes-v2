# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("Ex_GUI.ui", self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

if __name__ == "__main__":
    print("Here")