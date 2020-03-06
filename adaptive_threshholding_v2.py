# Author: Matthew C McFee
# Date: January 29, 2020
# Description: Immortalized MEndR staining is prone
# to variations in staining brightness. This script
# utilizes opencv's local thresholding to account for
# this weakness.

import cv2
import numpy as np
# import matplotlib.pyplot as plt
import easygui as eg
from os import listdir
from os import chdir

# Select a folder containing the images to be thresholded
dir_path = eg.diropenbox(msg = 'Select a folder with images')
chdir(dir_path)

# Generate the results text file
f = open('results.txt', "w")
f.write("File Surface Coverage Percentage" + "\n")

# Iterate throught he images in the folder and determine
# the surface coverage
for file in listdir(dir_path):
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    image = cv2.medianBlur(image, 5)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY, 11, 1)

    # After the image has be thresholded calculated the number of
    # pixels determined to be parts of fibres and count them
    # The surface coverage is % total pixels that are fibre pixels
    n_pix = np.sum(image > 0)
    num_total_px   = image.shape[0] * image.shape[1]
    thresh_area_pcnt = n_pix / num_total_px

    print(thresh_area_pcnt)
    f.write(file + " " + str(thresh_area_pcnt))
    f.write("\n")

f.close()
