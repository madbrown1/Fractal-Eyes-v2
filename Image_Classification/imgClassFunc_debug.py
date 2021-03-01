# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:02:19 2021

@author: Madellyn BRown
Image Classification function and debug
"""

import tensorflow as tf
from tensorflow import keras
import cv2

input_shape = (295,341) #Since image is only hrayscale

Voxel_shape = (1,1)

Voxel_path = r"C:\Users\THEma\Documents\ENGR498\Platelet\Augs\active\aug0.jpg"


for i in range(0,Voxel_shape[1]*Voxel_shape[0]-1, 1):
    img = cv2.imread(Voxel_path,cv2.IMREAD_GRAYSCALE) #edit for voxels
    if img.shape >= input_shape: #image voxel larger than training data
        Img_r = cv2.resize(img,input_shape, interpolation = cv2.INTER_AREA)
    else:
        Img_r = cv2.resize(img,input_shape, interpolation = cv2.INTER_LINEAR)
    
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array,0)
    
    model = keras.models.load_model('Insert file path mads')
    predictions = model.predict(img_array)
    if predictions[0] >= predictions:
        final_predict = 0 #not activated
    else:
        final_predict = 1 #activated
        cv2.imwrite("file location of activ_numVoxe"+str(i) + ".tif")
        
    
