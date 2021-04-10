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

import matplotlib.gridspec as gridspec

import feFunc


pd.set_option('display.max_columns', 100) ## Should make 100 columns of the DataFrame able to be displayed without cutting them out

GUI_list = ['pix_avg','area', 'perimeter', 'major_axis_length',
            'minor_axis_length','eccentricity','aspect_ratio',
            'perimeter_area_ratio','shading','pix_max','pix_min','avg_area',
            'avg_perimeter','avg_major_axis_length','avg_minor_axis_length',
            'avg_aspect_ratio', 'avg_perimeter_area_ratio','avg_eccentricity',
            'avg_shading','avg_pix_avg'] ## Make the list of each feature wanted for extraction (DEBUG). See the data_calculation function for complete list

n = 0
m = 0

## The code is separted for now into the interactive figure and gaining data in dataframes from manual thresholding. Both run, but the regions detected are different for now.
## The interactive figure uses a better method for region detection, and the manual thresholding only detects one region, though.

## Edit the code below with the correct path for whatever folder the subimages are in.
## Required File Structure (for now): Desktop -> Subimages -> PatientName -> SomeFolder -> subimage.tif
##                                               (Directory)  (Directory)    (Directory)  (image file, only one per folder)

## Main issue is thresholding and getting accurate regions


## Need to be gained from previous sections in the end - edit this section for images - works best with image A2.2 from "Chol_ENRandDEP" Images
path = 'C:/Users/Andrew/Desktop/011818 GFP on PCL/' 
patient = 'BigTest'

#Path for Patient folder
patientpath = path+patient


## Make sure Patient folder exists, if not: Program cannot continue 
if not os.path.exists(patientpath):
    raise Exception('File Error-No Patient Data')
    quit()
    
##Find all DIRECTORIES within Patient folder
Files = []
for (dirpath, dirnames, filenames) in walk(path+patient):
    Files.extend(dirnames)
    break

##Begin for loop that analyzes each subimage - iterates with each list item
for sub in Files:

    ##Filepath for Subimage folder
    Input = sub
    subpath = patientpath+'/'+sub
    
    ##Find all FILES within Subimage folder (Should make more specific to avoid error?)
    img_file = []
    for (dirpath, dirnames, filenames) in walk(subpath):
        img_file.extend(filenames)
        break
    ##There should be only one subimage per folder - if not, error in preprocessing. The program cannot continue
    if len(img_file)!= 1:
        raise Exception('Image Error-Too many subimages detected')
        quit()
    

    ## This will eventually need to run through a folder with a lot of other folders and images. We will need to get the name of the patient for the directory and standard naming
    img = cv2.imread(subpath+'/'+img_file[0],0)

    
    ##Filepath for new Features folder
    featurepath = subpath+'/Features'

    ##If it does not already exist, create the Features folder in the Subimage folder
    if not os.path.exists(featurepath):
        os.makedirs(featurepath)

    h,w = img.shape
    img_size = h*w

    m = m+1
    n = n+1

    labels = feFunc.binary_thresholding(img,n,m)
    table = feFunc.gain_regionprops(labels, img)
    table, grid_table = feFunc.data_calculation(table, GUI_list)
    feFunc.data_organization(table, grid_table, featurepath,n,m)


    i = 0
    j = 0
    size = len(GUI_list)
    x = np.arange(0,len(table.index),1)
    fig, ax = plt.subplots(4,5, figsize =(22,22))

    
    
    plt.setp(ax, xticks=x)


    width = 1
    
    for feature in GUI_list:

        if 'avg_' in feature:
            data1 = feFunc.data_retrieve(n,m,featurepath, feature)
            ax[i,j].bar(1, data1, width = 0.3, color = 'blue')
            ax[i,j].set_title(feature, y = 1.15)
        else:
            data1 = feFunc.data_retrieve(n,m,featurepath, feature)
            ax[i,j].bar(x, data1, width = 0.3, color = 'blue')
            ax[i,j].set_title(feature, y = 1.15)
        
        feFunc.add_value_labels(ax[i,j],5)
        i = i+1

        if i == 4:
            i = 0
            j = j+1


    plt.subplots_adjust(left=0.1, 
                    bottom=.1,  
                    right=0.9,  
                    top=.85,  
                    wspace=1,  
                    hspace=1)
    
    
    fig.savefig('C:/Users/Andrew/Desktop/Subimages Verify/Figures/'+'figure'+str(n)+'_'+str(m)+'.png')
    feFunc.save_data(n,m,table,'C:/Users/Andrew/Desktop/Subimages Verify/Data')
    feFunc.save_data(n,m,grid_table,'C:/Users/Andrew/Desktop/Subimages Verify/Data2')
    fig.clf()
    print("ImageDone "+str(n))


##
##    x = np.arange(0,len(table.index),1)
##    
##
##    fig, ax = plt.subplots(2,2)
##    plt.setp(ax, xticks=x)
##    ax[0,0].bar(x, table['area'],color = 'blue')
##    ax[0,0].set_title('Area')
##    ax[0,1].bar(x, p_over_a,color = 'blue')
##    ax[0,1].set_title('Perimeter/Area')
##    ax[1,0].bar(x, aspect_ratio,color = 'blue')
##    ax[1,0].set_title('Aspect Ratio')
##    ax[1,1].bar(x, table['eccentricity'],color = 'blue')
##    ax[1,1].set_title('Eccentricity')
##
##    plt.show()
##
##
##
##    plt.plot(np.max(img),np.min(img), 'bo')
##    plt.title('Min vs Max Pixel Values')
##    plt.ylabel('Min Pixel Value')
##    plt.xlabel('Max Pixel Value')
##    plt.show








    
    
    



