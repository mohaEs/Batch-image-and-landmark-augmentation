# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 11:58:55 2019

@author: Moha-Thinkpad
"""

## code for augmenting image + landmark locatios
# based on skimage
# and imgaug

from numpy import genfromtxt
Landmarks = genfromtxt('Landmarks.csv', delimiter=',')
Landmarks = Landmarks.astype(int)
Landmarks=Landmarks[1:] # remove the first row because it is just axis label

from skimage import io
Image = io.imread('Image.png')


#### visualization
import numpy as np

import matplotlib.pyplot as plt
plt.imshow(Image)
plt.plot(Landmarks[0,1],Landmarks[0,0],marker="s",color='red')
plt.plot(Landmarks[1,1],Landmarks[1,0],marker="s",color='red')
plt.plot(Landmarks[2,1],Landmarks[2,0],marker="s",color='red')
plt.plot(Landmarks[3,1],Landmarks[3,0],marker="s",color='red')
plt.plot(Landmarks[4,1],Landmarks[4,0],marker="s",color='red')


################# flip example
import imgaug as ia
from imgaug import augmenters as iaa


# The augmenters expect a list of imgaug.KeypointsOnImage.
keypoints_on_images = []
keypoints = []
for _ in range(len(Landmarks)):
    keypoints.append(ia.Keypoint(x=Landmarks[_,1], y=Landmarks[_,0]))
keypoints_on_images.append(ia.KeypointsOnImage(keypoints, shape=Image.shape))


flipper = iaa.Fliplr(1.0) # always horizontally flip each input image
transformed_image = flipper.augment_image(Image) # horizontally flip image 0
transformed_keypoints=flipper.augment_keypoints(keypoints_on_images)


X_new=[]
Y_new=[]
# Example code to show each image and print the new keypoints coordinates
for  keypoints_after in transformed_keypoints:
    for kp_idx, keypoint in enumerate(keypoints_after.keypoints):
        x_new, y_new = keypoint.x, keypoint.y
        X_new.append(x_new)
        Y_new.append(y_new)

newLandmarks=np.zeros(Landmarks.shape) 
newLandmarks[:,0]=np.asarray(Y_new)
newLandmarks[:,1]=np.asarray(X_new)
plt.imshow(transformed_image)
plt.plot(newLandmarks[0,1],newLandmarks[0,0],marker="s",color='red')
plt.plot(newLandmarks[1,1],newLandmarks[1,0],marker="s",color='red')
plt.plot(newLandmarks[2,1],newLandmarks[2,0],marker="s",color='red')
plt.plot(newLandmarks[3,1],newLandmarks[3,0],marker="s",color='red')
plt.plot(newLandmarks[4,1],newLandmarks[4,0],marker="s",color='red')


################# sequential example
import imgaug as ia
from imgaug import augmenters as iaa


# The augmenters expect a list of imgaug.KeypointsOnImage.
keypoints_on_images = []
keypoints = []
for _ in range(len(Landmarks)):
    keypoints.append(ia.Keypoint(x=Landmarks[_,1], y=Landmarks[_,0]))
keypoints_on_images.append(ia.KeypointsOnImage(keypoints, shape=Image.shape))


seq = iaa.Sequential([iaa.Fliplr(1, name="Flipper"), iaa.Affine(scale={"x": 0.9, "y": 0.9},  
                                       translate_percent={"x": 0.2, "y":  0.1},   
                                       rotate= 45  )])
seq_det = seq.to_deterministic() # call this for each batch again, NOT only once at the start

images=np.zeros(shape=[1,Image.shape[0],Image.shape[1]], dtype='uint8')
images[0,:,:]=Image
# augment keypoints and images
images_aug = seq_det.augment_images(images)
transformed_keypoints = seq_det.augment_keypoints(keypoints_on_images)

X_new=[]
Y_new=[]
# Example code to show each image and print the new keypoints coordinates
for  keypoints_after in transformed_keypoints:
    for kp_idx, keypoint in enumerate(keypoints_after.keypoints):
        x_new, y_new = keypoint.x, keypoint.y
        X_new.append(x_new)
        Y_new.append(y_new)

newLandmarks=np.zeros(Landmarks.shape) 
newLandmarks[:,0]=np.asarray(Y_new)
newLandmarks[:,1]=np.asarray(X_new)
plt.imshow(images_aug[0,:,:])
plt.plot(newLandmarks[0,1],newLandmarks[0,0],marker="s",color='red')
plt.plot(newLandmarks[1,1],newLandmarks[1,0],marker="s",color='red')
plt.plot(newLandmarks[2,1],newLandmarks[2,0],marker="s",color='red')
plt.plot(newLandmarks[3,1],newLandmarks[3,0],marker="s",color='red')
plt.plot(newLandmarks[4,1],newLandmarks[4,0],marker="s",color='red')


import os
from scipy import misc
write_to_dir = "."
misc.imsave(os.path.join(write_to_dir, 'transformed.png'), images_aug[0,:,:])
