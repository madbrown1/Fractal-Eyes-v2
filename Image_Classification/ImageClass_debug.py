# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 22:22:07 2021

@author: Madellyn Brown 
Senior Desing 21048
image classificaiton testing and debugging
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os

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
            start_y = numPixelRow*(y_h+1)
        
        start_x = numPixelCol*(x_w+1)
    return imgGrid

unprocess_dir = r"C:\Users\THEma\Documents\ENGR498\Platelet\unprocessed_img2"

#%% Create smaller images using 3x3 

# will create smaller datasets from images

numCol = 3
numRow = 3 

DirList = os.listdir(unprocess_dir)
newDir = r"C:\Users\THEma\Documents\ENGR498\Platelet\Processed_imgs2"
os.mkdir(newDir)

for i in range(0,len(DirList),1):
    img = cv2.imread(unprocess_dir +"\\" + DirList[i],cv2.IMREAD_GRAYSCALE)
    img = img[0:885,:] #crop bottom out
    voxels = VoxelCreate(numCol,numRow, img)
    n = 1
    for x in range(0,numCol, 1):
        for y in range(0,numRow,1):
            cv2.imwrite(newDir + '\\' +str(n)+'-' + DirList[i], voxels[y][x])
            #maintain original number
            n = n + 1
            
#%% modify data using tensorflow 
FullActive_dir = r"C:\Users\THEma\Documents\ENGR498\Platelet\Full_Active"

PartActive_dir = r"C:\Users\THEma\Documents\ENGR498\Platelet\Partial_Active"

Rest_dir = r"C:\Users\THEma\Documents\ENGR498\Platelet\Resting"

DirList = os.listdir(Rest_dir)
newDir =Rest_dir + r"\augs"
os.mkdir(newDir)

data_augmentation = tf.keras.Sequential([
  layers.experimental.preprocessing.RandomFlip("horizontal_and_vertical"),
  layers.experimental.preprocessing.RandomRotation(0.1),
])

for i in range(0,len(DirList),1):
    img = cv2.imread(Rest_dir +"\\" + DirList[i],cv2.IMREAD_COLOR)
    img = tf.expand_dims(img,0)
    
    for ii in range(9):
        aug_img = data_augmentation(img)
        cv2.imwrite(newDir + '\\' +'AUG'+str(ii) +'_'+ str(i) + ".jpg",aug_img[0].numpy().astype("uint8"))
#%% rename images to letnum        
dir1 = r"C:\Users\THEma\Documents\ENGR498\Platelet\aug\NonActiveimgsaug"

dir2 = r"C:\Users\THEma\Documents\ENGR498\Platelet\Augs\nonactive"

DirList = os.listdir(dir1)
for i in range(0,len(DirList),1):
    img = cv2.imread(dir1+"\\" + DirList[i], cv2.IMREAD_COLOR)
    cv2.imwrite(dir2 +"\\aug" + str(i) + ".jpg",img) 
    #os.rename(dir2 +"\\" + DirList[i],dir2 +"\\aug" + str(i) + ".tif")
    

#%% train on top of augmented stuff in three classes 
image_size = (295,341)
batch_size = 16
img_dir = r'C:\Users\THEma\Documents\ENGR498\Platelet\augTHREE'
train_ds = ds = tf.keras.preprocessing.image_dataset_from_directory(
    img_dir,
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="categorical",
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    img_dir,
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
    label_mode="categorical",
)

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)

base_model = tf.keras.applications.InceptionV3(
    input_shape = (295,341, 3),
    include_top=False,
    weights="imagenet",
    )

base_model.trainable = False

inputs = keras.Input(shape=(295,341, 3))

x = base_model(inputs, training = False)
x = keras.layers.experimental.preprocessing.Rescaling(1./255)(x)
x = keras.layers.GlobalAveragePooling2D()(x)

outputs = keras.layers.Dense(3,activation="softmax")(x)

model = keras.Model(inputs, outputs)

model.compile(optimizer = keras.optimizers.Adam(),
              loss = keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics = ["accuracy"])

#%%
image_size = (295,341)
batch_size = 16
img_dir = r'C:\Users\THEma\Documents\ENGR498\Platelet\Augs'
train_ds = ds = tf.keras.preprocessing.image_dataset_from_directory(
    img_dir,
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    img_dir,
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)

base_model = tf.keras.applications.InceptionV3(
    input_shape = (295,341, 3),
    include_top=False,
    weights="imagenet",
    )

base_model.trainable = False

inputs = keras.Input(shape=(295,341, 3))

x = base_model(inputs, training = False)

x = keras.layers.experimental.preprocessing.Rescaling(1./255)(x)

x = keras.layers.GlobalAveragePooling2D()(x)

outputs = keras.layers.Dense(1)(x)

model = keras.Model(inputs, outputs)

model.compile(optimizer = keras.optimizers.Adam(),
              loss = keras.losses.BinaryCrossentropy(from_logits=True),
              metrics = ["accuracy"])
#%%%
for i in range(5,35,5):
    his = model.fit(train_ds, epochs = i, validation_data=val_ds)
    plt.figure()
    plt.subplot(221)
    plt.plot(his.history['accuracy'])  
    plt.plot(his.history['val_accuracy'])  
    plt.title('model accuracy')  
    plt.ylabel('accuracy')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'valid']) 
    
    plt.subplot(222)  
    plt.plot(his.history['loss'])  
    plt.plot(his.history['val_loss'])  
    plt.title('model loss')  
    plt.ylabel('loss')  
    plt.xlabel('epoch')  
    plt.legend(['train', 'valid']) 
    
    plt.show()
