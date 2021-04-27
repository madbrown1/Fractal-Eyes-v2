import numpy as np
import os.path
import cv2
import os
from os import walk
import pandas as pd

import tensorflow as tf
from tensorflow import keras

from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate
from skimage import data, filters, measure, morphology
from fractions import Fraction
from matplotlib.ticker import NullFormatter

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


def test(string):
    print(string)

def Feature_Extraction():
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

    # Path for Patient folder
    patientpath = path + patient

    ## Make sure Patient folder exists, if not: Program cannot continue
    if not os.path.exists(patientpath):
        raise Exception('File Error-No Patient Data')
        quit()

    ##Find all DIRECTORIES within Patient folder
    Files = []
    for (dirpath, dirnames, filenames) in walk(path + patient):
        Files.extend(dirnames)
        break

    ##Begin for loop that analyzes each subimage - iterates with each list item
    for sub in Files:

        ##Filepath for Subimage folder
        Input = sub
        subpath = patientpath + '/' + sub

        ##Find all FILES within Subimage folder (Should make more specific to avoid error?)
        img_file = []
        for (dirpath, dirnames, filenames) in walk(subpath):
            img_file.extend(filenames)
            break
        ##There should be only one subimage per folder - if not, error in preprocessing. The program cannot continue
        if len(img_file) != 1:
            raise Exception('Image Error-Too many subimages detected')
            quit()

        ## This will eventually need to run through a folder with a lot of other folders and images. We will need to get the name of the patient for the directory and standard naming
        img = cv2.imread(subpath + '/' + img_file[0], 0)

        ##Make sure the images are correct (DEBUG)
        cv2.imshow("A1.1", img)
        cv2.waitKey(500)
        cv2.destroyAllWindows()

        ##Filepath for new Features folder
        featurepath = subpath + '/Features'

        ##If it does not already exist, create the Features folder in the Subimage folder
        if not os.path.exists(featurepath):
            os.makedirs(featurepath)

        ##Determine Threshold and Erosion/Dilation polygon
        thresh = 175  # For manual
        threshold = filters.threshold_otsu(img)  # Automatic
        kernel = np.ones((10, 10), np.uint8)

        ##For Organization - This should activate the interactive figure
        ##Thresholding
        img_over = img > threshold
        img_out = morphology.remove_small_objects(img_over, 3, in_place=True)
        img_out = morphology.remove_small_holes(img_over, 3)
        labels = measure.label(img_out)

        ##Set up figure
        fig = px.imshow(img, binary_string=True)
        fig.update_traces(hoverinfo='skip')  # hover is only for label info

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
        contour, hier = cv2.findContours(img_threshold, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        ##Fill Contours
        for cnt in contour:
            cv2.drawContours(img_threshold, [cnt], 0, 255, -1)

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
        pix = open(featurepath + '/pixelval', "wb")
        table.to_pickle(featurepath + '/propsval')

        ##Save the pixel values to the file (pixel values will be in array format)
        np.save(pix, img)

        ##Check (DEBUG)
        df = pd.read_pickle(featurepath + '/propsval')

        print(df)

        plt.scatter(df['area'], df['perimeter'])
        plt.show()


def VoxelCreate(numCol, numRow, img):
    #This function will divide the image into user col and row voxels 
    img =  img[:,:,1]
    #Grab current size of image
    w , h= img.shape
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

def tri4Voxel(voxels, numCol, numRow):
    out_voxels = [[0 for x in range(numCol)] for y in range(numRow)]

    for y in range(0, numRow, 1):
        for x in range(0, numCol, 1):
            voxel_shape = voxels[y][x].shape
            white = 255;
            mask = np.zeros(voxel_shape, dtype=np.uint8)  # creates base mask
            # triangle 1
            pts1 = np.array([[[0, 0], [int(voxel_shape[1] / 2), int(voxel_shape[0] / 2)], [0, voxel_shape[0]]]])
            cv2.fillPoly(mask, pts1, white)
            mask_vox1 = cv2.bitwise_and(voxels[0][0], mask)

            # triangle 2
            mask = np.zeros(voxel_shape, dtype=np.uint8)
            pts2 = np.array([[[0, 0], [int(voxel_shape[1] / 2), int(voxel_shape[0] / 2)], [voxel_shape[1], 0]]])
            cv2.fillPoly(mask, pts2, white)
            mask_vox2 = cv2.bitwise_and(voxels[0][0], mask)

            # triangle 3
            mask = np.zeros(voxel_shape, dtype=np.uint8)
            pts3 = np.array([[[voxel_shape[1], 0], [int(voxel_shape[1] / 2), int(voxel_shape[0] / 2)],
                              [voxel_shape[1], voxel_shape[0]]]])
            cv2.fillPoly(mask, pts3, white)
            mask_vox3 = cv2.bitwise_and(voxels[0][0], mask)

            # triangle 4
            mask = np.zeros(voxel_shape, dtype=np.uint8)
            pts4 = np.array([[[0, voxel_shape[0]], [int(voxel_shape[1] / 2), int(voxel_shape[0] / 2)],
                              [voxel_shape[1], voxel_shape[0]]]])
            cv2.fillPoly(mask, pts4, white)
            mask_vox4 = cv2.bitwise_and(voxels[0][0], mask)

            # combine all masks and save under each voxel(row,col, tri num)
            Tri_comb = np.dstack((mask_vox1, mask_vox2, mask_vox3, mask_vox4))
            out_voxels[y][x] = Tri_comb

    return out_voxels

def tri2UPVoxel(voxels,numCol,numRow):
    out_voxels =  [[0 for x in range(numCol)] for y in range(numRow)]
    
    for y in range(0,numRow,1):
        for x in range(0,numCol,1):
            
            voxel_shape = voxels[y][x].shape
            white = 255; 
            mask = np.zeros(voxel_shape, dtype = np.uint8) #creates base mask as same shape of voxel
            
            #triangle 1
            pts1 =  np.array([[[0,0],[voxel_shape[1],0], [0,voxel_shape[0]]]])
            cv2.fillPoly(mask, pts1, white) 
            mask_vox1 = cv2.bitwise_and(voxels[y][x],mask)
            
            #triangle 2 
            mask =  np.zeros(voxel_shape, dtype = np.uint8)
            pts2 = np.array([[[voxel_shape[1],voxel_shape[0]],[voxel_shape[1],0], [0,voxel_shape[0]]]])
            cv2.fillPoly(mask, pts2, white)
            mask_vox2 = cv2.bitwise_and(voxels[y][x],mask)
            
            #combine all masks and save under each voxel(row,col, tri num)
            Tri_comb = np.dstack((mask_vox1,mask_vox2))
            out_voxels[y][x] = Tri_comb
            
    return out_voxels

def tri2DOWNVoxel(voxels,numCol,numRow):
    out_voxels =  [[0 for x in range(numCol)] for y in range(numRow)]
    
    for y in range(0,numRow,1):
        for x in range(0,numCol,1):
            
            voxel_shape = voxels[y][x].shape
            white = 255; 
            mask = np.zeros(voxel_shape, dtype = np.uint8) #creates base mask as same shape of voxel
            
            #triangle 1
            pts1 =  np.array([[[0,0],[voxel_shape[1],0], [voxel_shape[1],voxel_shape[0]]]])
            cv2.fillPoly(mask, pts1, white) 
            mask_vox1 = cv2.bitwise_and(voxels[y][x],mask)
            
            #triangle 2 
            mask =  np.zeros(voxel_shape, dtype = np.uint8)
            pts2 = np.array([[[0,0],[0,voxel_shape[0]],[voxel_shape[1],voxel_shape[0]]]])
            cv2.fillPoly(mask, pts2, white)
            mask_vox2 = cv2.bitwise_and(voxels[y][x],mask)
            
            #combine all masks and save under each voxel(row,col, tri num)
            Tri_comb = np.dstack((mask_vox1,mask_vox2))
            out_voxels[y][x] = Tri_comb
            
    return out_voxels

def CircleVoxel(voxels, numCol,numRow):  
    out_voxels =  [[0 for x in range(numCol)] for y in range(numRow)]
    
    for y in range(0,numRow,1):
        for x in range(0,numCol,1):
            voxel_shape = voxels[y][x].shape
            mask = np.zeros(voxel_shape, dtype = np.uint8) #creates base mask
            
            x_center = int(voxel_shape[1]/2)
            y_center = int(voxel_shape[0]/2)
            radius = y_center if y_center < x_center else x_center

            cv2.circle(mask,(x_center,y_center), radius, 255,-1)

            mask_vox = cv2.bitwise_and(voxels[y][x],mask)
            out_voxels[y][x] = mask_vox
            #out_voxels shape is [numCol][numRow]
            
    return out_voxels
    
def binary_thresholding(vox): ##Create binary mask and labels - only labels are output

    if vox.ndim > 2:
        vox = vox[:,:,1]

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

    ##Increase Image Contrast and Brightness
    vox = cv2.normalize(vox, None, alpha=.5, beta=1.9, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    vox = np.clip(vox, 0, 1)
    vox = (255*vox).astype(np.uint8)

    
    ##Determine Threshold and Erosion/Dilation polygon
    threshold = filters.threshold_otsu(vox) #Automatic        

    ##Threshold the Image and Erode/Dilate
    th, vox_threshold = cv2.threshold(vox, threshold, 255, cv2.THRESH_BINARY)
    ##Circle Kernel Erode/Dilate for smooother lines and to connect polygons
    kernel_circle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3),(-1,-1))
    vox_threshold = cv2.dilate(vox_threshold, kernel_circle, iterations=10)
    vox_threshold = cv2.erode(vox_threshold, kernel_circle, iterations=9)
  

    ##Find Contours
    contour, hier = cv2.findContours(vox_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ##Fill Contours
    for cnt in contour:
        cv2.drawContours(vox_threshold,[cnt],0,255,-1)
    labels = measure.label(vox_threshold)

    return labels

def ImgClass(numCol,numRow,voxels):
    input_shape = (295,341) #For Machine Learning model
    #input number of rows/column and voxels that have been created

    dirname = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    modelfilename = os.path.join(dirname, 'Image_Classification\Inceptionv3_3class')



    model = keras.models.load_model(modelfilename)
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
            print(predictions) #[full,partial, rest]

            Final_Predict[y,x] = np.argmax(predictions)
            # 0 = Full  Active
            # 1 = Partial Active
            # 2 = Resting 
            
    return Final_Predict.tolist()

def gain_regionprops(regions, vox): ##gain basic data values from each label
    
    ##Create Empty Arrays
    pix_avg = []
    pix_min = []
    pix_max = []

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
        pix_min.append(np.min(pixels))
        pix_max.append(np.max(pixels))

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
        if 'avg_' in feature:
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
            if 'shading' in table.columns:
                avg_shading = table['shading'].mean()
            else:
                shading = table['pix_max'] - table['pix_min']
                avg_shading = shading.mean()
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

    

def save_data(n, m, path):
    
    gainfile_v = path+'/voxel_values'+str(n)+'_'+str(m)
    gainfile_g = path+'/gvg_values'+str(n)+'_'+str(m)
    data = pd.read_pickle(gainfile_v)
    data2 = pd.read_pickle(gainfile_g)
    data2.to_csv(path+'/Save_GvG'+str(n)+'_'+str(m)+'.csv')
    data.to_csv(path+'/Save_Vox'+str(n)+'_'+str(m)+'.csv')

    return
