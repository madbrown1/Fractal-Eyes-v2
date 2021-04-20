# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:02:19 2021

@author: Madellyn BRown
Image Classification function and debug
"""

import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np
import matplotlib.pyplot as plt


def VoxelCreate(numCol, numRow, img):
    #This function will divide the image into user col and row voxels 
    
    #Grab current size of image
    w , h = img.shape
    #Find pixel length and witdh for each grid
    numPixelCol = int(w/numCol)
    numPixelRow = int(h/numRow)

    #Grid images, note final grid will be in form of y,x due to line 40 arrangement
    imgGrid = [[0 for x in range(numCol)] for y in range(numRow)] 
    start_x = 0
    for x_w in range(0, numCol, 1):
        start_y = 0
        #print("start_x: " + str(start_x)) #Check for correct position
    
        for y_h in range(0, numRow, 1):
            #print("start_y: " + str(start_y)) #Check for correct position
            # grid part works as from the from start til entire length of subgrid
            #Length of voxel is dependent on what position of the grid it is in
            
            imgGrid[y_h][x_w] = img[start_x:numPixelCol*(x_w+1),start_y:numPixelRow*(y_h+1)]
            imgGrid[y_h][x_w]/255 #normalize the image
            start_y = numPixelRow*(y_h+1)
        
        start_x = numPixelCol*(x_w+1)
    return imgGrid

input_shape = (295,341) #Since image is only hrayscale

Voxel_shape = (2,2)

Voxel_path = r"C:\Users\THEma\Documents\ENGR498\Platelet Data\Original Images\Image32_32.png"
IMG = cv2.imread(Voxel_path,cv2.IMREAD_GRAYSCALE) #edit for voxels
voxels = VoxelCreate(2,2,IMG)

#%% 
model = keras.models.load_model(r'C:\Users\THEma\Documents\GitHub\Fractal-Eyes-v2\Image_Classification\Inceptionv3_3class')

#%%
numCol = 2
numRow = 2
Final_Predict = np.zeros((numRow,numRow))

for x in range(0,2,1):
    for y in range(0,2,1):
        plt.figure()
        plt.imshow(voxels[y][x])
        img = np.dstack((voxels[y][x], voxels[y][x], voxels[y][x]))
    
        if img.shape >= input_shape: #image voxel larger than training data
            Img_r = cv2.resize(img,input_shape, interpolation = cv2.INTER_AREA)
        else:
            Img_r = cv2.resize(img,input_shape, interpolation = cv2.INTER_LINEAR)
         #add create 3 dim image
        img_array = keras.preprocessing.image.img_to_array(Img_r)
        img_array = tf.expand_dims(img_array,0)
        
        predictions = model.predict(img_array)
        print(predictions) #[full,partial, rest]

        Final_Predict[y,x] = np.argmax(predictions)
        # 0 = Full  Active
        # 1 = Partial Active
        # 2 = Resting 

#%% Define function

def ImgClass(numCol,numRow,voxels):
    #input number of rows/column and voxels that have been created
    model = keras.models.load_model(r'C:\Users\THEma\Documents\GitHub\Fractal-Eyes-v2\Image_Classification\Inceptionv3_3class')
    Final_Predict = np.zeros((numRow,numRow))
    
    for x in range(0,numCol,1):
        for y in range(0,numRow,1):
            img = np.dstack((voxels[y][x], voxels[y][x], voxels[y][x]))
            
            if img.shape >= input_shape: #image voxel larger than training data
                Img_r = cv2.resize(img,input_shape, interpolation = cv2.INTER_AREA)
            else:
                Img_r = cv2.resize(img,input_shape, interpolation = cv2.INTER_LINEAR)
            #add create 3 dim image
            img_array = keras.preprocessing.image.img_to_array(Img_r)
            img_array = tf.expand_dims(img_array,0)
        
            predictions = model.predict(img_array)
            #print(predictions) #[full,partial, rest]

            Final_Predict[y,x] = np.argmax(predictions)
            # 0 = Full  Active
            # 1 = Partial Active
            # 2 = Resting 
            
    return Final_Predict.tolist()

