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



pd.set_option('display.max_columns', 100)


## The code is separted for now into the interactive figure and gaining data in dataframes from manual thresholding. Both run, but the regions detected are different for now.
## The interactive figure uses a better method for region detection, and the manual thresholding only detects one region, though.

## Edit the code below with the correct path for whatever folder the subimages are in.
## Required File Structure (for now): Desktop -> Subimages -> PatientName -> SomeFolder -> subimage.tif
##                                               (Directory)  (Directory)    (Directory)  (image file, only one per folder)

## Main issue is thresholding and getting accurate regions


## Need to be gained from previous sections in the end - edit this section for images - works best with image A2.2 from "Chol_ENRandDEP" Images
path = 'C:/Users/Andrew/Desktop/Subimages/'
patient = 'A2.2'

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

    ##Make sure the images are correct (DEBUG)
    cv2.imshow("A1.1",img)
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    
    ##Filepath for new Features folder
    featurepath = subpath+'/Features'

    ##If it does not already exist, create the Features folder in the Subimage folder
    if not os.path.exists(featurepath):
        os.makedirs(featurepath)

    ##Determine Threshold and Erosion/Dilation polygon
    thresh = 175 #For manual
    threshold = filters.threshold_otsu(img) #Automatic
    kernel= np.ones((10,10), np.uint8)

 
    ##For Organization - This should activate the interactive figure
        ##Thresholding
    img_over = img > threshold
    img_out = morphology.remove_small_objects(img_over, 3, in_place = True)
    img_out = morphology.remove_small_holes(img_over, 3)
    labels = measure.label(img_out)

        ##Set up figure
    fig = px.imshow(img, binary_string=True)
    fig.update_traces(hoverinfo='skip') # hover is only for label info
    
        ##Will compute regions when each is used, use "_table" to compute them all now, may have to to save data
    props = measure.regionprops(labels, img)
    properties = ['centroid',
                  'area',
                  'perimeter',
                  'major_axis_length',
                  'minor_axis_length',
                  'eccentricity']


        ##Activate and populate figure
    for index in range(1, labels.max()):
        label = props[index].label
        contour = measure.find_contours(labels == label, 0.5)[0]
        y, x = contour.T
        hoverinfo = ''
        for prop_name in properties:
            hoverinfo = hoverinfo + prop_name + ': '
            hoverinfo = hoverinfo + str({getattr(props[index], prop_name)})
            hoverinfo = hoverinfo + '\n'
            print(hoverinfo)
        fig.add_trace(go.Scatter(
            x=x, y=y, name=label,
            mode='lines', fill='toself', showlegend=False,
            hovertemplate=hoverinfo, hoveron='points+fills'))
        
        ##Figure should display in browser for now
    fig.show()
    

    ##Threshold the Image and Erode/Dilate - Based on Manual and Data Frames
    th, img_threshold = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    img_threshold = cv2.dilate(img_threshold, kernel, iterations=5)
    img_threshold = cv2.erode(img_threshold, kernel, iterations=5)
    

    ##Find Contours
    contour,hier = cv2.findContours(img_threshold,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    ##Fill Contours
    for cnt in contour:
        cv2.drawContours(img_threshold,[cnt],0,255,-1)



    cv2.imshow("Foreground", img_threshold)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    props = regionprops_table(img_threshold, properties=('centroid',
                                                 'area',
                                                 'perimeter',
                                                 'major_axis_length',
                                                 'minor_axis_length',
                                                 'eccentricity'))

    table = pd.DataFrame(props)

    ##Open a write file in the Features folder(binary)
    pix = open(featurepath+'/pixelval', "wb")
    table.to_pickle(featurepath+'/propsval')
    
    ##Save the pixel values to the file (pixel values will be in array format)
    np.save(pix,img)

    ##Check (DEBUG)
    df = pd.read_pickle(featurepath+'/propsval')

    print(df)

    plt.scatter(df['area'], df['perimeter'])
    plt.show()

