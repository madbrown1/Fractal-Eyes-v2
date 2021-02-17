import numpy as np
import os.path
import cv2
import os
from os import walk
import pandas as pd

from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate
from skimage import data, filters, measure, morphology


import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from fractions import Fraction
from matplotlib.ticker import NullFormatter



def binary_thresholding(vox): ##Create binary mask and labels - only labels are output
    
    ##Determine Threshold and Erosion/Dilation polygon
    threshold = filters.threshold_otsu(vox) #Automatic        

    ##Threshold the Image and Erode/Dilate
    th, vox_threshold = cv2.threshold(vox, threshold, 255, cv2.THRESH_BINARY)
    kernel= np.ones((10,10), np.uint8)
    vox_threshold = cv2.dilate(vox_threshold, kernel, iterations=5)
    vox_threshold = cv2.erode(vox_threshold, kernel, iterations=5)
    

    ##Find Contours
    contour,hier = cv2.findContours(vox_threshold,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    ##Fill Contours
    for cnt in contour:
        cv2.drawContours(vox_threshold,[cnt],0,255,-1)
    labels = measure.label(vox_threshold)

    cv2.imshow("thresh",vox_threshold)
    cv2.waitKey(500)

    return labels



def gain_regionprops(regions, vox): ##gain basic data values from each label
    
    ##Create Empty Arrays
    pix_avg=[]
    pix_min=[]
    pix_max=[]

    ##Extract Basic Features
    props = regionprops_table(regions, properties=('centroid',
                                                 'area',
                                                 'perimeter',
                                                 'major_axis_length',
                                                 'minor_axis_length',
                                                 'eccentricity'))
    ##Convert to DataFrame
    table = pd.DataFrame(props)

 

    ##Find Pixel Values in Each Region
    for i in range(1, np.amax(regions)+1):
        locs = np.where(regions == i)

        pixels = vox[locs]
        
        pix_avg.append(np.average(pixels))
        pix_min.append(min(pixels))
        pix_max.append(max(pixels))

    ##Calculate Pixel Data
    table.loc[:,'pix_avg'] = pix_avg
    table.loc[:,'pix_max'] = pix_max
    table.loc[:,'pix_min'] = pix_min

    ##For now, filter out small areas with hardcoded value
    table = table[table['area']>50]

    return table



def data_calculation(table, feature_list): ##Advanced data, based on list input
    cols = []
    for feature in feature_list: ##Determine if the GvG DataFrame will contain data
        if 'avg' in feature:
            cols.append(feature)
    if not cols:
        cols = ['none']            
    gvg = pd.DataFrame(columns = cols, index=range(1))    ##Create GvG DataFrame
    for feature in feature_list: ##Calculate all necessary features
        if feature == 'aspect_ratio':
            aspect_ratio = table['minor_axis_length']/table['major_axis_length']
            table.loc[:,'aspect_ratio'] = aspect_ratio
            
        elif feature == 'perimeter_area_ratio':
            p_over_a = table['perimeter']/table['area']
            table.loc[:,'perimeter_area_ratio'] = p_over_a
            
        elif feature == 'shading':
            shading = table['pix_max'] - table['pix_min']
            table.loc[:,'shading'] = shading
                       
        elif feature == 'avg_area':
            avg_area = table['area'].mean()
            gvg.loc[:,'avg_area'] = avg_area

        elif feature == 'avg_perimeter':
            avg_perimeter = table['perimeter'].mean()
            gvg.loc[:,'avg_perimeter'] = avg_perimeter
            
        elif feature == 'avg_major_axis_length':
            avg_major_axis_length = table['major_axis_length'].mean()
            gvg.loc[:,'avg_major_axis_length'] = avg_major_axis_length

        elif feature == 'avg_minor_axis_length':
            avg_minor_axis_length = table['minor_axis_length'].mean()
            gvg.loc[:,'avg_minor_axis_length'] = avg_minor_axis_length

        elif feature == 'avg_eccentricity':
            avg_eccentricity = table['eccentricity'].mean()
            gvg.loc[:,'avg_eccentricity'] = avg_eccentricity

        elif feature == 'avg_aspect_ratio':
            avg_aspect_ratio = table['aspect_ratio'].mean()
            gvg.loc[:,'avg_aspect_ratio'] = avg_aspect_ratio

        elif feature == 'avg_perimeter_area_ratio':
            avg_perimeter_area_ratio = table['perimeter_area_ratio'].mean()
            gvg.loc[:,'avg_perimeter_area_ratio'] = avg_perimeter_area_ratio

        elif feature == 'avg_shading':
            avg_shading = table['shading'].mean()
            gvg.loc[:,'avg_shading'] = avg_shading

        elif feature == 'avg_pix_avg':
            avg_pix_avg = table['pix_avg'].mean()
            gvg.loc[:,'avg_pix_avg'] = avg_pix_avg

        elif feature == 'avg_pix_min':
            avg_pix_min = table['pix_min'].mean()
            gvg.loc[:,'avg_pix_min'] = avg_pix_min

        elif feature == 'avg_pix_max':
            avg_pix_max = table['pix_max'].mean()
            gvg.loc[:,'avg_pix_max'] = avg_pix_max
        
    return table, gvg                                                                                                     

        
            
def data_organization(vox_vals, GvG_vals, path): ##Serialize and save data for other subsystems
    
    ##If GvG_vals is empty, do no save it. If it is not,
    ##save it in the save input directory as vox_vals.
    if 'none' in GvG_vals:
        vox_vals.to_pickle(path + '/voxel_values')
    else:
        vox_vals.to_pickle(path + '/voxel_values')
        GvG_vals.to_pickle(path + '/gvg_values')
        
    return
    
        


