# -*- coding: utf-8 -*-
#%% 
"""
Created on Fri Dec 11 16:49:49 2020

@author: madbrown1@email.arizona.edu
Test plot of data collected from three different types of platelets
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

fp_Mech = r"C:\Users\THEma\Documents\ENGR498\KeraTesting\3_platelets\Mechanically activated platelets\sonicated, 10sec(3).tif"

fp_non = r"C:\Users\THEma\Documents\ENGR498\KeraTesting\3_platelets\non-activated\untreated(16).tif"

fp_ADP = r"C:\Users\THEma\Documents\ENGR498\KeraTesting\3_platelets\platelets activated by ADP\A1.3.tif"

mech_img = cv2.imread(fp_Mech,cv2.IMREAD_GRAYSCALE) 
non_img =  cv2.imread(fp_non,cv2.IMREAD_GRAYSCALE)
ADP_img = cv2.imread(fp_ADP,cv2.IMREAD_GRAYSCALE)

#%% create image voxels

#User Selected grid
# numCol = 1
# numRow = 1


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
    
def tri4Voxel(voxels, numCol,numRow):  
    out_voxels =  [[0 for x in range(numCol)] for y in range(numRow)]
    
    for y in range(0,numRow,1):
        for x in range(0,numCol,1):
            
            voxel_shape = voxels[y][x].shape
            white = 255; 
            mask = np.zeros(voxel_shape, dtype = np.uint8) #creates base mask
            #triangle 1
            pts1 =  np.array([[[0,0],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [0,voxel_shape[0]]]])
            cv2.fillPoly(mask, pts1, white) 
            mask_vox1 = cv2.bitwise_and(voxels[y][x],mask)
            
            #triangle 2 
            mask =  np.zeros(voxel_shape, dtype = np.uint8)
            pts2 = np.array([[[0,0],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [voxel_shape[1],0]]])
            cv2.fillPoly(mask, pts2, white)
            mask_vox2 = cv2.bitwise_and(voxels[y][x],mask)

            #triangle 3
            mask =  np.zeros(voxel_shape, dtype = np.uint8)
            pts3 = np.array([[[voxel_shape[1],0],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [voxel_shape[1],voxel_shape[0]]]])
            cv2.fillPoly(mask, pts3, white)
            mask_vox3 = cv2.bitwise_and(voxels[y][x],mask)
            
            #triangle 4
            mask =  np.zeros(voxel_shape, dtype = np.uint8)
            pts4 = np.array([[[0,voxel_shape[0]],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [voxel_shape[1],voxel_shape[0]]]])
            cv2.fillPoly(mask, pts4, white)
            mask_vox4 = cv2.bitwise_and(voxels[y][x],mask)
            
            #combine all masks and save under each voxel(row,col, tri num)
            Tri_comb = np.dstack((mask_vox1,mask_vox2,mask_vox3,mask_vox4))
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

#%% Plot images and proper way to loop through in order to display
numCol = 5
numRow = 4
voxels = VoxelCreate(numCol, numRow, ADP_img)
plt.figure()
i = 1; 

for x in range(0,numCol, 1):
    for y in range(0,numRow,1):
      
            plt.subplot(numCol,numRow,i)
            #print(i)
            plt.imshow(voxels[y][x])
            i = i +1

#%% 2 triangles up direction 
numCol = 1
numRow = 1
voxels = VoxelCreate(numCol, numRow, ADP_img)

voxel_shape = voxels[0][0].shape #grabs voxel shape
mask =  np.zeros(voxel_shape, dtype = np.uint8) #creates base mask
white = 255; 


#triangle 1
pts1 =  np.array([[[0,0],[voxel_shape[1],0], [0,voxel_shape[0]]]])
cv2.fillPoly(mask, pts1, white) 

mask_vox1 = cv2.bitwise_and(voxels[0][0],mask)
plt.figure()
plt.imshow(mask_vox1)

#Triangle 2 
mask =  np.zeros(voxel_shape, dtype = np.uint8)
pts2 = np.array([[[voxel_shape[1],voxel_shape[0]],[voxel_shape[1],0], [0,voxel_shape[0]]]])

cv2.fillPoly(mask, pts2, white)

mask_vox2 = cv2.bitwise_and(voxels[0][0],mask)

plt.figure()
plt.imshow(mask_vox2)


#%% 2 triangles down direction
numCol = 1
numRow = 1
voxels = VoxelCreate(numCol, numRow, ADP_img)

voxel_shape = voxels[0][0].shape #grabs voxel shape
mask =  np.zeros(voxel_shape, dtype = np.uint8) #creates base mask
white = 255; 

#triangle 1
pts1 =  np.array([[[0,0],[voxel_shape[1],0], [voxel_shape[1],voxel_shape[0]]]])
cv2.fillPoly(mask, pts1, white) 

mask_vox1 = cv2.bitwise_and(voxels[0][0],mask)
plt.figure()
plt.imshow(mask_vox1)

#Triangle 2 
mask =  np.zeros(voxel_shape, dtype = np.uint8)
pts2 = np.array([[[0,0],[0,voxel_shape[0]],[voxel_shape[1],voxel_shape[0]]]])

cv2.fillPoly(mask, pts2, white)

mask_vox2 = cv2.bitwise_and(voxels[0][0],mask)

plt.figure()
plt.imshow(mask_vox2)

#%% circle voxels debug

numCol = 1
numRow = 1
voxels = VoxelCreate(numCol, numRow, ADP_img)
voxel_shape = voxels[0][0].shape #grabs voxel shape
mask =  np.zeros(voxel_shape, dtype = np.uint8) #creates base mask
white = 255; 

x_center = int(voxel_shape[1]/2)
y_center = int(voxel_shape[0]/2)

radius = y_center if y_center < x_center else x_center

cv2.circle(mask,(x_center,y_center), radius, 255,-1)

mask_vox = cv2.bitwise_and(voxels[0][0],mask)
    
plt.figure()
plt.imshow(mask_vox)


    

#%% 4 triangles for each voxel function

numCol = 2
numRow = 2
voxels = VoxelCreate(numCol, numRow, ADP_img)

#outtest = tri4Voxel(voxels,numCol,numRow)
# plt.imshow(outtest[0][0][:,:,0]) Access data in correct format

i = 1; 
for y in range(0,numRow,1):
    for x in range(0,numCol, 1):
      
            plt.subplot(numCol,numRow,i)
            #print(i)
            plt.imshow(voxels[y][x])
            i = i +1
            
            
#%% voxel debug
numCol = 2
numRow = 3
img =  ADP_img

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
        start_y = numPixelRow*(y_h+1)
    
    start_x = numPixelCol*(x_w+1)


#%% Create triangle voxels for DEGUB 

# voxel_shape = voxels[0][0].shape #grabs voxel shape
# mask =  np.zeros(voxel_shape, dtype = np.uint8) #creates base mask
# white = 255; 
# #calculates and rounds to voxel center
# vox_center = np.array([[int(voxel_shape[0]/2), int(voxel_shape[1]/2)]])

# #triangle 1
# pts1 =  np.array([[[0,0],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [0,voxel_shape[0]]]])
# cv2.fillPoly(mask, pts1, white) 

# mask_vox1 = cv2.bitwise_and(voxels[0][0],mask)
# plt.figure()
# plt.imshow(mask_vox1)

# #Triangle 2 
# mask =  np.zeros(voxel_shape, dtype = np.uint8)
# pts2 = np.array([[[0,0],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [voxel_shape[1],0]]])

# cv2.fillPoly(mask, pts2, white)

# mask_vox2 = cv2.bitwise_and(voxels[0][0],mask)

# plt.figure()
# plt.imshow(mask_vox2)

# # Triangle 3 
# mask =  np.zeros(voxel_shape, dtype = np.uint8)
# pts3 = np.array([[[voxel_shape[1],0],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [voxel_shape[1],voxel_shape[0]]]])

# cv2.fillPoly(mask, pts3, white)
# mask_vox3 = cv2.bitwise_and(voxels[0][0],mask)
# plt.figure()
# plt.imshow(mask_vox3)

# # Triangle 4 
# mask =  np.zeros(voxel_shape, dtype = np.uint8)
# pts4 = np.array([[[0,voxel_shape[0]],[int(voxel_shape[1]/2), int(voxel_shape[0]/2)], [voxel_shape[1],voxel_shape[0]]]])
# cv2.fillPoly(mask, pts4, white)
# mask_vox4 = cv2.bitwise_and(voxels[0][0],mask)
# plt.figure()
# plt.imshow(mask_vox4)