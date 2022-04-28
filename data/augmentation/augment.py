import cv2
from augmentations import rotate, shear, adaptive_thresh, texturize, gaussian_noise

import argparse
import sys
import os.path
import os
import glob
import random
import re

# augmentation test script

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="augmentation test script")
    p.add_argument('--symbol_folder', type=str, help="Directory containing symbol images", required=True)
    args = p.parse_args(sys.argv[1:])

    args.symbol_folder = os.path.abspath(args.symbol_folder)

    imglist = os.listdir(args.symbol_folder)
    imglist = [os.path.join(args.symbol_folder, img) for img in imglist if re.search(r'.*\.(jpg|png)', img, re.IGNORECASE)]
    cv2.namedWindow("test")
    texture = cv2.imread("textures/bg_addon/crumpled3.png", cv2.IMREAD_UNCHANGED)

    for imgname in imglist:
        img = cv2.imread(imgname)
        mask = adaptive_thresh(img)
        img[mask != 0] = 255  # masked image
        img = rotate(img, random.randint(0, 180))
        img = shear(img, random.randint(-20, 20))
        img = texturize(img, texture)
        cv2.imshow("test",img)
        cv2.imshow("test", gaussian_noise(img))
        cv2.waitKey(0)
