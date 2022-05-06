#Takes image as input and outputs augmented version of it

import numpy as np
import cv2
import random
from random import randint
from scipy import ndimage

#When rotation-, transformation_dir- or thickness_dir = None then rotation, direction in randomly picked
#
#transformation dir = 0 means the top left corner of the right triangle is shifted.
#transformation dir = 1 means the top right corner of the right triangle is shifted.
#transformation dir = 2 means the bottom left corner of the right triangle is shifted.
#
#thickness_dir = 1 means dilation
#thickness_dir = -1 means erosion
#
#add_noise = True means that random pixels on image are changed to black.
#noise_threshold is value for which the uniform distribution value for pixel must be higher in order it to change black.

def generate(img, apply_resize = False, resize_str = 20, apply_flip = False, flip_random = True, apply_rotation = False, rotation = None, apply_transformation = False, transformation_dir = None, apply_thickness = False, thickness_dir = None, add_noise = False, noise_threshold = 0.999, scale_to_binary = False):
    #Select random image subclass
    #Randomize the size of the image
    if apply_resize:
        img = cv2.resize(img, [randint(img.shape[1]-resize_str,img.shape[1]+resize_str),randint(img.shape[0]-resize_str,img.shape[0]+resize_str)])
    #Flip the image along vertical axis.
    if apply_flip:
        if flip_random:
            if randint(0,1) == 0:
                img = cv2.flip(img,1)
        else:
            img = cv2.flip(img,1)
    #Randomize the rotation of the image.
    if apply_rotation:
        if rotation == None:
            rotation = randint(0,359)
        img = ndimage.rotate(img, randint(0,359), mode='constant',cval=255)
    if apply_transformation:
        #Add padding for affine transformation. Otherwise the picture might not be in bounds.
        img = np.pad(img, (100, 100), 'constant', constant_values=(255, 255))
        #Originial right triangle
        pts1 = np.float32([[3,3],[3,10],[10,3]])
        if transformation_dir == None:
            transformation_dir = randint(0,2)
        if transformation_dir == 0:
            pts2 = np.float32([[randint(1,5),randint(1,5)],[3,10],[10,3]])
        if transformation_dir == 1:
            pts2 = np.float32([[3,3],[randint(1,5),randint(8,12)],[10,3]])
        if transformation_dir == 2:
            pts2 = np.float32([[3,3],[3,10],[randint(8,12),randint(1,5)]])
        #Get transformation
        M = cv2.getAffineTransform(pts1,pts2)
        #Apply transformation
        img  = cv2.warpAffine(img ,M,(img.shape[1],img.shape[0]),borderValue = 255)
    #Remove excess rows and columns that appeared after rotation and padding
    img = img[np.argwhere(np.amin(img,axis=1) < 140)[0][0]:np.argwhere(np.amin(img,axis=1) < 140)[-1][0],:]
    img = img[:,np.argwhere(np.amin(img,axis=0) < 140)[0][0]:np.argwhere(np.amin(img,axis=0) < 140)[-1][0]]
    img = cv2.resize(img, [100,100]) #Resize back to 100x100
    
    #dilation and erosion
    if apply_thickness:
    #If randint = 2, then we apply neither.
        kernel = np.ones((3,3),np.uint8) #Kernel 3x3 seemed to work fine.
        if thickness_dir == None:
            thickness_dir = randint(-1,1) #If 0 we apply neither.
        if thickness_dir == 1: #erode 1 iteration. #OpenCV erodes white to black. In our case function erode actually dilates.
            img = cv2.erode(img,kernel,iterations = 1)
        if thickness_dir == -1:
            img = cv2.dilate(img,kernel,iterations = 1)
    
    #Apply noise by changing random pixels to one.
    if add_noise:
        img[np.random.rand(img.shape[0],img.shape[1]) > noise_threshold] = 0
    
    #Changes all the pixels with drawing to one and all the "empty" pixels to 0.
    if scale_to_binary:
        img[img <= 140] = 1
        img[img > 140] = 0
    
    return img