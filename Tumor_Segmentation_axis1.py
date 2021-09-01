# -*- coding: utf-8 -*-
"""Copy of LastPracAxi1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17EV09kHwIfwp5JNNWnmGwIUkhpMTsyoP
"""

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import tensorflow as tf
import keras
import keras.backend as K
from keras.utils import to_categorical
from keras import metrics
from keras.models import Model, load_model
from keras.layers import Input, BatchNormalization, Activation, Dense, Dropout,Maximum
from keras.layers.core import Lambda, RepeatVector, Reshape
from keras.layers.convolutional import Conv2D, Conv2DTranspose,Conv3D,Conv3DTranspose
from keras.layers.pooling import MaxPooling2D, GlobalMaxPool2D,MaxPooling3D
from keras.layers.merge import concatenate, add
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from skimage.io import imread, imshow, concatenate_images
from skimage.transform import resize
from sklearn.utils import class_weight


from keras.callbacks import ModelCheckpoint
from keras.callbacks import CSVLogger
from keras.callbacks import EarlyStopping

import os
from skimage.io import imread, imshow, concatenate_images
from skimage.transform import resize
# from medpy.io import load
import numpy as np

#import cv2
import nibabel as nib
from PIL import Image

def conv_block(input_mat,num_filters,kernel_size,batch_norm):
  X = Conv2D(num_filters,kernel_size=(kernel_size,kernel_size),strides=(1,1),padding='same')(input_mat)
  if batch_norm:
    X = BatchNormalization()(X)
 
  X = Activation('relu')(X)

  X = Conv2D(num_filters,kernel_size=(kernel_size,kernel_size),strides=(1,1),padding='same')(X)
  if batch_norm:
    X = BatchNormalization()(X)
 
  X = Activation('relu')(X)
 
  return X

def Unet_with_slice(input_img, n_filters = 16 , dropout = 0.3 , batch_norm = True):
  c1 = Conv2D(16,kernel_size = (1,6) , strides = (1,1) ,padding = 'valid')(input_img)
  if batch_norm:
    c1 = BatchNormalization()(c1)
  #print(c1.shape)
  c1 = Activation('relu')(c1)

  c1 = Conv2D(n_filters,kernel_size=(3,3),strides=(1,1),padding='same')(c1)
  if batch_norm:
    c1 = BatchNormalization()(c1)
 
  c1 = Activation('relu')(c1)

  p1 = MaxPooling2D(pool_size = (2,2) , strides = 2)(c1)
  p1 = Dropout(dropout)(p1)

  #print(p1.shape)
  c2 = conv_block(p1 , n_filters*2,3,batch_norm)
  p2 = MaxPooling2D(pool_size=(3,3), strides=3)(c2)
  p2 = Dropout(dropout)(p2)
  #print(p2.shape)

  c3 = conv_block(p2, n_filters*4,3,batch_norm)
  #print(c3.shape)
  p3 = MaxPooling2D(pool_size = (2,1) , strides = (2,1))(c3)
  p3 = Dropout(dropout)(p3)
  #print(p3.shape)

  c4 = conv_block(p3, n_filters*8,3,batch_norm)
  p4 = MaxPooling2D(pool_size = (4,4) , strides = (4,5))(c4)
  p4 = Dropout(dropout)(p4)

  c5 = conv_block(p4,n_filters*16,3,batch_norm)

  u6 = Conv2DTranspose(n_filters*8,kernel_size = (4,4) , strides = (4,5) , padding = 'same')(c5)
  u6 = concatenate([u6,c4])
  c6 = conv_block(u6,n_filters*8,3,batch_norm)
  c6 = Dropout(dropout)(c6)

  u7 = Conv2DTranspose(n_filters*4,kernel_size = (3,3) , strides = (2,1) , padding = 'same')(c6)
  u7 = concatenate([u7,c3])
  c7 = conv_block(u7,n_filters*4,3,batch_norm)
  c7 = Dropout(dropout)(c7)

  u8 = Conv2DTranspose(n_filters*2,kernel_size = (3,3) , strides = (3,3) , padding = 'same')(c7)
  u8 = concatenate([u8,c2])
  c8 = conv_block(u8,n_filters*2,3,batch_norm)
  c8 = Dropout(dropout)(c8)

  u9 = Conv2DTranspose(n_filters,kernel_size = (3,3) , strides = (2,2) , padding = 'same')(c8)
  u9 = concatenate([u9,c1])
  c9 = conv_block(u9,n_filters,3,batch_norm)
  c9 = Dropout(dropout)(c9)

  c10 = Conv2DTranspose(n_filters, kernel_size = (1,6) , strides = (1,1), padding = 'valid')(c9)

  outputs = Conv2D(4, kernel_size = (1,1), activation = 'softmax')(c10)

  model = Model(inputs = input_img , outputs = outputs)

  return model



def standardize(image):

  standardized_image = np.zeros(image.shape)

  #
 
      # iterate over the `z` dimension
  for z in range(image.shape[2]):
      # get a slice of the image
      # at channel c and z-th dimension `z`
      image_slice = image[:,:,z]

      # subtract the mean from image_slice
      centered = image_slice - np.mean(image_slice)
     
      # divide by the standard deviation (only if it is different from zero)
      if(np.std(centered)!=0):
          centered = centered/np.std(centered)

      # update  the slice of standardized image
      # with the scaled centered and scaled image
      standardized_image[:, :, z] = centered

  ### END CODE HERE ###

  return standardized_image


def dice_coef(y_true, y_pred, epsilon=0.00001):
    """
    Dice = (2*|X & Y|)/ (|X|+ |Y|)
         =  2*sum(|A*B|)/(sum(A^2)+sum(B^2))
    ref: https://arxiv.org/pdf/1606.04797v1.pdf
   
    """
    axis = (0,1,2)
    dice_numerator = 2. * K.sum(y_true * y_pred, axis=axis) + epsilon
    dice_denominator = K.sum(y_true*y_true, axis=axis) + K.sum(y_pred*y_pred, axis=axis) + epsilon
    return K.mean((dice_numerator)/(dice_denominator))

def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)


input_img = Input((240,155,4))
model = Unet_with_slice(input_img,32,0.15,True)
learning_rate = 0.00095
#epochs = 5000
decay_rate = 0.0000002
model.compile(optimizer=Adam(lr=learning_rate, decay = decay_rate), loss=dice_coef_loss, metrics=[dice_coef])
model.summary()


path = '/content/drive/MyDrive/BRATS2018TRAIN/HGG'
all_images = os.listdir(path)
#print(len(all_images))
all_images.sort()
data = np.zeros((240,240,155,4))
image_data2=np.zeros((240,240,155))
loss_hist = []
accu_hist = []
epoch_wise_loss = []
epoch_wise_accu = []
for epochs in range(45):
  epoch_loss = 0
  epoch_accu = 0
  for image_num in range(180):
    x_to = []
    y_to = []
    print(epochs)
    print(image_num)

# data preprocessing starts here

    x = all_images[image_num]
    print(x)
    folder_path = path + '/' + x;
    modalities = os.listdir(folder_path)
    modalities.sort()
    #data = []
    w = 0
    for j in range(len(modalities)):
      #print(modalities[j])
     
      image_path = folder_path + '/' + modalities[j]
      if not(image_path.find('seg.nii') == -1):
        img = nib.load(image_path);
        image_data2 = img.get_data()
        image_data2 = np.asarray(image_data2)
        print("Entered ground truth")
      else:
        img = nib.load(image_path);
        image_data = img.get_data()
        image_data = np.asarray(image_data)
        image_data = standardize(image_data)
        data[:,:,:,w] = image_data
        print("Entered modality")
        w = w+1
     
    print(data.shape)
    print(image_data2.shape)  
   
    '''
    reshaped_data=data[56:184,75:203,13:141,:]
    reshaped_data=reshaped_data.reshape(1,128,128,128,4)
    reshaped_image_data2=image_data2[56:184,75:203,13:141]

       
    reshaped_image_data2=reshaped_image_data2.reshape(1,128,128,128)
    reshaped_image_data2[reshaped_image_data2==4] = 3
    hello = reshaped_image_data2.flatten()
    #y_to = keras.utils.to_categorical(y_to,num_classes=2)
    print(reshaped_image_data2.shape)
    #print(hello[hello==3].shape)
    print("Number of classes",np.unique(hello))
    class_weights = class_weight.compute_class_weight('balanced',np.unique(hello),hello)
    print(class_weights)
   
   
    '''
   
   
    for slice_no in range(0,240):
        a = slice_no
        X = data[slice_no,:,:,:]

        Y = image_data2[slice_no,:,:]
        # imgplot = plt.imshow(X[:,:,2])
        # plt.show(block=False)
        # plt.pause(0.3)
        # plt.close()

        # imgplot = plt.imshow(Y)
        # plt.show(block=False)
        # plt.pause(0.3)
        # plt.close()

        if(X.any()!=0 and Y.any()!=0 and len(np.unique(Y)) == 4):
          #print(slice_no)
          x_to.append(X)
          y_to.append(Y)
          if len(y_to)>=50:
                break;

        #reshaped_image_data2 = to_categorical(reshaped_image_data2, num_classes = 4)

        #print(reshaped_data.shape)
        #print(reshaped_image_data2.shape)
        #print(type(reshaped_data))

    x_to = np.asarray(x_to)
    y_to = np.asarray(y_to)
    print(x_to.shape)
    print(y_to.shape)

 
    y_to[y_to==4] = 3        
    #y_to = one_hot_encode(y_to)
    #y_to[y_to==2] = 1
    #y_to[y_to==1] = 1
    #y_to[y_to==0] = 0
    print(y_to.shape)
   
   
    from sklearn.utils import shuffle
    x_to,y_to = shuffle(x_to,y_to)
   
    hello = y_to.flatten()
    #print(hello[hello==3].shape)
    print("Number of classes",np.unique(hello))
    class_weights = class_weight.compute_class_weight('balanced',np.unique(hello),hello)
 
    #class_weights.insert(3,0)
    print("class_weights",class_weights)
   

    y_to = keras.utils.to_categorical(y_to,num_classes=4)
    history = model.fit(x=x_to,y=y_to, epochs = 1 , batch_size = 50)
    print(history.history['loss'])
    epoch_loss += history.history['loss'][0]
    epoch_accu += history.history['dice_coef'][0]
   
    loss_hist.append(history.history['loss'])
    accu_hist.append(history.history['dice_coef'])
 
  model.save('/content/drive/MyDrive/models/2d_Lastprac_axis1.h5')
  epoch_loss = epoch_loss/180
  epoch_accu = epoch_accu/180

  epoch_wise_loss.append(epoch_loss)
  epoch_wise_accu.append(epoch_accu)
 
  plt.plot(epoch_wise_loss)
  plt.title('Model_loss vs epochs')
  plt.ylabel('Loss')
  plt.xlabel('epochs')
  s = '/content/drive/MyDrive/SAVEFIG/epochwise_loss_Lastpracaxis1s' + str(epochs)
  plt.savefig(s)
  plt.show()
  plt.close()
 
  plt.plot(epoch_wise_accu)
  plt.title('Model_Accuracy vs epochs')
  plt.ylabel('Accuracy')
  plt.xlabel('epochs')
  s = '/content/drive/MyDrive/SAVEFIG/epochwise_accu_Lastpracaxis1s' + str(epochs)
  plt.savefig(s)
  plt.show()
  plt.close()
   
  plt.plot(accu_hist)
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  s = '/content/drive/MyDrive/SAVEFIG/accuracy_plot_Lastpracaxis1s' + str(epochs)
  plt.savefig(s)
  plt.show()
  plt.close()
   
  plt.plot(loss_hist)
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  s = '/content/drive/MyDrive/SAVEFIG/loss_plot_Lastpracaxis1s' + str(epochs)
  plt.savefig(s)
  plt.show()
  plt.close()

model.save('/content/drive/MyDrive/models/2d_Lastprac_axis1.h5')