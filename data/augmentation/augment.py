import cv2

from augmentations import rotate, shear, adaptive_thresh

import argparse
import sys
import os.path
import glob

# augmentation test script

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="augmentation test script")
    p.add_argument('--symbol_folder', type=str, help="Directory containing symbol images", required=True)
    args = p.parse_args(sys.argv[1:])

    args.symbol_folder = os.path.abspath(args.symbol_folder)

    imglist = glob.glob(args.symbol_folder + "/*.JPG")
    cv2.namedWindow("test")

    for imgname in imglist:
        img = cv2.imread(imgname)
        cv2.imshow("test", adaptive_thresh(img))
        cv2.waitKey(0)
