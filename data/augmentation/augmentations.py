import cv2
import numpy as np
import random


def shear(img, degs):
    """shears <degs> degrees in the x direction"""
    negative = degs < 0  # if negative, shear in the other direction
    rads = abs(degs) * np.pi/180
    shear_matrix = np.array([[1., rads, 0],
                            [0,  1.,   0],
                            [0,  0,    1.]])
    h, w, _ = img.shape
    nw = w + rads*h

    if negative:
        img = cv2.flip(img, 0)

    img = cv2.warpPerspective(img, shear_matrix, (int(nw), h), borderValue=(255, 255, 255))

    if negative:
        img = cv2.flip(img, 0)
    return img


def rotate(img, degs):
    h, w, _ = img.shape
    rot_matrix = cv2.getRotationMatrix2D(center=(w//2, h//2), angle=degs, scale=1.)
    cos, sin = abs(rot_matrix[0, 0]), abs(rot_matrix[0, 1])
    nw = int(h*sin + w*cos)
    nh = int(h*cos + w*sin)
    rot_matrix[0, 2] += (nw//2) - w//2
    rot_matrix[1, 2] += (nh//2) - h//2

    img = cv2.warpAffine(img,
                         rot_matrix,
                         (nw, nh),
                         borderMode=cv2.BORDER_CONSTANT,
                         borderValue=(255, 255, 255))
    return img


def adaptive_thresh(img):
    # returns a black-and-white 1 channel
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return img


def texturize(img, texture):
    h, w, _ = img.shape
    th, tw, _ = texture.shape
    print(h, w, th, tw)
    chosen_h, chosen_w = random.randint(0, th-h-1), random.randint(0, tw-w-1)
    tex_crop = texture[chosen_h:chosen_h+h, chosen_w:chosen_w+w, 3]
    # TODO: change this 0.7 to something more reasonable
    return np.clip(cv2.addWeighted(tex_crop,
                                   1.0,
                                   cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                                   0.7,
                                   10),
                   0, 255)


def color_shift(img):
    pass

def gaussian_noise(img)


# for testing
# img = cv2.imread("../generator/destroy1.jpg")
# cv2.namedWindow("a")
# cv2.imshow("a", rotate(img, 30))
# cv2.waitKey(0)
