import cv2
import numpy as np


def shear(img, degs):
    """shears <degs> degrees in the x direction"""
    negative = degs < 0  # if negative, shear in the other direction
    rads = abs(degs) * np.pi/180
    shear_matrix = np.array([[1., rads, 0],
                            [0,  1.,   0],
                            [0,  0,    1.]])
    w, h, _ = img.shape
    nw = w + rads*h

    if negative:
        img = cv2.flip(img, 0)

    img = cv2.warpPerspective(img, shear_matrix, (int(nw), h))

    if negative:
        img = cv2.flip(img, 0)
    return img


def rotate(img, degs):
    h, w, _ = img.shape
    rot_matrix = cv2.getRotationMatrix2D(center=(w/2, h/2), angle=degs, scale=1.)
    cos, sin = abs(rot_matrix[0, 0]), abs(rot_matrix[0, 1])
    nw = int(h*sin + w*cos)
    nh = int(h*cos + w*sin)
    rot_matrix[0, 2] += (nw//2) - w//2
    rot_matrix[1, 2] += (nh//2) - h//2

    img = cv2.warpAffine(img, rot_matrix, (nw, nh))
    return img

def texturize(img):
    pass

def color_shift(img):
    pass


# for testing
# img = cv2.imread("../generator/destroy1.jpg")
# cv2.namedWindow("a")
# cv2.imshow("a", rotate(img, 30))
# cv2.waitKey(0)
