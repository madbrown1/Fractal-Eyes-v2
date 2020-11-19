# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:06:50 2020

@author: Madellyn Brown
## This script is to test the matplotlib.pyplot and opencv for importing an
## an image and applying a grid
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np
import pillow as PIL

#local file path of image
fp = r"C:\Users\THEma\Documents\ENGR498\KeraTesting\C1.5.tif"

#read image into memory
img = cv2.imread(fp, cv2.IMREAD_GRAYSCALE)
# cv2.imshow('window',img)
# cv2.waitKey()

#User Selected grid
numCol = 2
numRow = 2

#Grab current size of image
w , h =img.shape

#Find pixel length and witdh for each grid
numPixelCol = int(w/numCol)
numPixelRow = int(h/numRow)

#Grid images
mGrid = [[0 for x in range(numCol)] for y in range(numRow)]
for x_w in range(0,w, numPixelCol):
    for y_h in range(0 , h, numPixelRow):
        




