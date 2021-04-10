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

import time

from PIL import Image, ImageEnhance


def binary_thresholding(vox,n,m): ##Create binary mask and labels - only labels are output


    
    ##Gaussian Blur to reduce noise
    vox = cv2.GaussianBlur(vox,(7,7),0)
   
    ##Filter salt and pepper noise
    count = 0
    lastMedian = vox
    median = cv2.medianBlur(vox, 3)
    while not np.array_equal(lastMedian, median):
        # get those pixels that gets zeroed out
        zeroed = np.invert(np.logical_and(median, vox))
        vox[zeroed] = 0

        count = count + 1
        if count > 50:
            break
        lastMedian = median
        median = cv2.medianBlur(vox, 3)



    vox = cv2.normalize(vox, None, alpha=.5, beta=1.5, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    vox = np.clip(vox, 0, 1)
    vox = (255*vox).astype(np.uint8)
    
    ##Determine Threshold and Erosion/Dilation polygon
    
    threshold = filters.threshold_otsu(vox) #Automatic
    #vox_threshold = cv2.adaptiveThreshold(vox,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #cv2.THRESH_BINARY,111,2)
    

    ##Threshold the Image and Erode/Dilate
    th, vox_threshold = cv2.threshold(vox, threshold, 255, cv2.THRESH_BINARY)
    kernel= np.ones((5,5), np.uint8)
    kernel_circle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3),(-1,-1))
    vox_threshold = cv2.dilate(vox_threshold, kernel_circle, iterations=7)
    vox_threshold = cv2.erode(vox_threshold, kernel_circle, iterations=7)




        

    ##Find Contours
    contour,hier = cv2.findContours(vox_threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)            
            
    
    
    ##Fill Contours
    for contourIdx, cnt in enumerate(contour):        
            cv2.drawContours(vox_threshold,[cnt],0,255,-1)
        
        
            
    labels = measure.label(vox_threshold)

    
    cv2.imwrite('C:/Users/Andrew/Desktop/Subimages Verify/Threshold/thresh'+str(n)+'_'+str(m)+'.png',vox_threshold)
    
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
    m_area = int(table['area'].mean())
    table = table[table['area']>(m_area / 16)]

     

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
            if 'aspect_ratio' in table.columns:
                avg_aspect_ratio = table['aspect_ratio'].mean()                
            else:
                aspect_ratio = table['minor_axis_length']/table['major_axis_length']
                avg_aspect_ratio = aspect_ratio.mean()
                
            gvg.loc[:,'avg_aspect_ratio'] = avg_aspect_ratio

        elif feature == 'avg_perimeter_area_ratio':
            if 'perimeter_area_ratio' in table.columns:
                avg_perimeter_area_ratio = table['perimeter_area_ratio'].mean()
            else:
                p_over_a = table['perimeter']/table['area']
                avg_perimeter_area_ratio = p_over_a.mean()
                
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

    if not 'centroid' in feature_list:
        del table['centroid-1']
        del table['centroid-0']
        
    if not 'area' in feature_list:
        del table['area']

    if not 'perimeter' in feature_list:
        del table['perimeter']
        
    if not 'eccentricity' in feature_list:
        del table['eccentricity']

    if not 'major_axis_length' in feature_list:
        del table['major_axis_length']
        
    if not 'minor_axis_length' in feature_list:
        del table['minor_axis_length']      



        
    return table, gvg                                                                                                     

        
            
def data_organization(vox_vals, GvG_vals, path, n, m): ##Serialize and save data for other subsystems
    
    ##If GvG_vals is empty, do no save it. If it is not,
    ##save it in the save input directory as vox_vals.
    if 'none' in GvG_vals:
        vox_vals.to_pickle(path + '/voxel_values'+str(n)+'_'+str(m))
    else:
        vox_vals.to_pickle(path + '/voxel_values'+str(n)+'_'+str(m))
        GvG_vals.to_pickle(path + '/gvg_values'+str(n)+'_'+str(m))
        
    return
    
def data_retrieve(n, m, featurepath, feature_string):

    gainfile_v = featurepath+'/voxel_values'+str(n)+'_'+str(m)
    gainfile_g = featurepath+'/gvg_values'+str(n)+'_'+str(m)
    

    if 'avg_' in feature_string:
        if not os.path.exists(gainfile_g):
            raise Exception('Required Grid vs. Grid data does not exist')
            quit()
        else:
            table = pd.read_pickle(gainfile_g)
            data = table._get_value(0,feature_string)
    else:
        if not os.path.exists(gainfile_v):
            raise Exception('Required Voxel Region data does not exist')
            quit()
        else:
            table = pd.read_pickle(gainfile_v)
            data = table[feature_string]
        
        
    return data   

    

def save_data(n, m, data, path):
    
    data.to_csv(path+'/Save'+str(n)+'_'+str(m)+'.csv')

    return

def add_value_labels(ax, spacing):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.



