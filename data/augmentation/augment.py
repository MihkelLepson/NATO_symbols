import cv2
from augmentations import rotate, shear, adaptive_thresh, texturize

import argparse
import sys
import os.path
import glob
import random

# augmentation test script

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="augmentation test script")
    p.add_argument('--symbol_folder', type=str, help="Directory containing symbol images", required=True)
    args = p.parse_args(sys.argv[1:])

    args.symbol_folder = os.path.abspath(args.symbol_folder)

    imglist = glob.glob(args.symbol_folder + "/*.JPG")
    cv2.namedWindow("test")
    texture = cv2.imread("textures/bg_addon/crumpled3.png", cv2.IMREAD_UNCHANGED)

    for imgname in imglist:
        img = cv2.imread(imgname)
        mask = adaptive_thresh(img)
        img[mask != 0] = 255  # masked image
        img = rotate(img, random.randint(0, 180))
        img = shear(img, random.randint(-20, 20))
        cv2.imshow("test", texturize(img, texture))
        cv2.waitKey(0)
