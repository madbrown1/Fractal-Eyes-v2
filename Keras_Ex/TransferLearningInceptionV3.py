# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 03:14:35 2020

@author: Madellyn Brown
This py script will be the process for transfer training a binary classifier
based the dataset https://data.mendeley.com/datasets/snkd93bnjr/1
on a inceptionv3 model and a mobileNet model in keras

"""

import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
## Generate data set
image_size = (360, 363)
batch_size = 16

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    r"C:\Users\THEma\Documents\ENGR498\KeraTesting\TransferTest",
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    r"C:\Users\THEma\Documents\ENGR498\KeraTesting\TransferTest",
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)

train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)

base_model = tf.keras.applications.VGG16(
    include_top=False,
    weights="imagenet",
    input_shape = (360, 363, 3),
    )

base_model.trainable = False

inputs = keras.Input(shape= (360,363,3))

x = base_model(inputs, training = False)

x = keras.layers.GlobalAveragePooling2D()(x)

outputs = keras.layers.Dense(1)(x)

model = keras.Model(inputs, outputs)

model.compile(optimizer = keras.optimizers.Adam(),
              loss = keras.losses.BinaryCrossentropy(from_logits=True),
              metrics = ["accuracy"])
his = model.fit(train_ds, epochs = 5, validation_data=val_ds)

#%%
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