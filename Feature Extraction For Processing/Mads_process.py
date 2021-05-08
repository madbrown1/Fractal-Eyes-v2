# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 21:59:58 2021

@author: THEma
Process images for each individual folder and save out data
"""

import os
import cv2
import feFunc

Dir_platelets = [r"C:\Users\THEma\Documents\ENGR498\Platelet\Full_Active",
                 r"C:\Users\THEma\Documents\ENGR498\Platelet\Partial_Active",
                 r"C:\Users\THEma\Documents\ENGR498\Platelet\Resting"]

GUI_list = ['pix_avg','area', 'perimeter', 'major_axis_length',
            'minor_axis_length','eccentricity','aspect_ratio',
            'perimeter_area_ratio','shading','pix_max','pix_min','avg_area',
            'avg_perimeter','avg_major_axis_length','avg_minor_axis_length',
            'avg_aspect_ratio', 'avg_perimeter_area_ratio','avg_eccentricity',
            'avg_shading','avg_pix_avg']

for k in range(0,len(Dir_platelets),1):
    DirList = os.listdir(Dir_platelets[k])
    n = 1
    m = 1
    
    for i in range(0,len(DirList),1):
        img = cv2.imread(Dir_platelets[k] + "\\" +DirList[i], cv2.IMREAD_GRAYSCALE)
        h, w = img.shape
        img_size = h*w
        labels = feFunc.binary_thresholding(img,n,m)
        table = feFunc.gain_regionprops(labels,img)
        table, grid_table = feFunc.data_calculation(table,GUI_list)
        
        #check to make sure data path is present 
        if not os.path.exists(Dir_platelets[k]+r"\Data"):
            os.makedirs(Dir_platelets[k]+r"\Data")
            
        feFunc.save_data(n,m,table,Dir_platelets[k]+r"\Data")
        n = n+1
        m = m+1
        
    
    
        
# threshold = filters.threshold_otsu(vox)
#th, vox_threshold = cv2.threshold(vox, threshold, 255, cv2.THRESH_BINARY)

    
    
    
        
        