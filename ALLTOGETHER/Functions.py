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
    # This function will divide the image into user col and row voxels

    # Grab current size of image
    w, h = img.shape
    # Find pixel length and witdh for each grid
    numPixelCol = int(w / numCol)
    numPixelRow = int(h / numRow)

    # Grid images, note final grid will be in form of y,x due to line 40 arrangement
    imgGrid = [[0 for x in range(numCol)] for y in range(numRow)]
    start_x = 0
    for x_w in range(0, numCol, 1):
        start_y = 0
        # print("start_x: " + str(start_x)) #Check for correct position

        for y_h in range(0, numRow, 1):
            # print("start_y: " + str(start_y)) #Check for correct position
            # grid part works as from the from start til entire length of subgrid
            # Length of voxel is dependent on what position of the grid it is in

            imgGrid[x_w][y_h] = img[start_x:numPixelCol * (x_w + 1), start_y:numPixelRow * (y_h + 1)]
            start_y = numPixelRow * (y_h + 1)

        start_x = numPixelCol * (x_w + 1)
    return imgGrid


def plotVoxelImages():# %% Plot images
    numCol = 1
    numRow = 1
    voxels = VoxelCreate(numCol, numRow, ADP_img)
    plt.figure()
    i = 1;
    for y in range(0, numRow, 1):
        for x in range(0, numCol, 1):
            plt.subplot(numCol, numRow, i)
            # print(i)
            plt.imshow(voxels[y][x])
            i = i + 1

    # %% 2 triangles up dir
    numCol = 1
    numRow = 1
    voxels = VoxelCreate(numCol, numRow, ADP_img)

    voxel_shape = voxels[0][0].shape  # grabs voxel shape
    mask = np.zeros(voxel_shape, dtype=np.uint8)  # creates base mask
    white = 255;

    # #triangle 1
    # pts1 =  np.array([[[0,0],[voxel_shape[1],0], [0,voxel_shape[0]]]])
    # cv2.fillPoly(mask, pts1, white)

    # mask_vox1 = cv2.bitwise_and(voxels[0][0],mask)
    # plt.figure()
    # plt.imshow(mask_vox1)

    # Triangle 2
    mask = np.zeros(voxel_shape, dtype=np.uint8)
    pts2 = np.array([[[voxel_shape[1], voxel_shape[0]], [voxel_shape[1], 0], [0, voxel_shape[0]]]])

    cv2.fillPoly(mask, pts2, white)

    mask_vox2 = cv2.bitwise_and(voxels[0][0], mask)

    plt.figure()
    plt.imshow(mask_vox2)


# %% 4 triangles for each voxel function

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

def Plot4Voxel():
    numCol = 2
    numRow = 2
    voxels = VoxelCreate(numCol, numRow, ADP_img)

    outtest = tri4Voxel(voxels, numCol, numRow)
    # plt.imshow(outtest[0][0][:,:,0]) Access data in correct format

    i = 1;
    for y in range(0, numRow, 1):
        for x in range(0, numCol, 1):
            plt.subplot(numCol, numRow, i)
            # print(i)
            plt.imshow(voxels[y][x])
            i = i + 1
