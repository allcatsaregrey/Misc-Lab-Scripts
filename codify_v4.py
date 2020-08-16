# Author: Matthew C. McFee
# Date: January 30, 2020
# Description: A simple python script to codify file names for generating
# ground truth datasets. The script currently only works with .oib and .oif
# file formats.

# TODO: Adapt the script to be able to rename files in a folder hierarchy and
# generalize the script to work with all filetypes. Fix the numbering issues
# due to folders being present

import numpy as np
import easygui as eg
import os
import json

# Select a folder of images to codify
dir_path = eg.diropenbox(msg='Select a folder with images to codify')
os.chdir(dir_path)

# Initialize an empty dictionary to store file name and associated key
# and generate an initial set of codes from 1 to 40
results = {}
files = os.listdir(dir_path)
length = len(files)

# Count the number of oif files and remove these from the range
# to make the numbers make sense.

num_folders = len([file for file in os.listdir(dir_path)
                   if file.endswith('.files')])
print(num_folders)

indices = list(range(1, length - num_folders + 1))
indices_array = np.array(indices)

# Get the list of file names and cycle through the files
for file in os.listdir(dir_path):

    if file.endswith('.oib'):
        code = int(np.random.choice(indices_array))
        results[file] = code
        os.rename(file, str(code) + ".oib")
        indices_array = indices_array[indices_array != code]

# Handle the fact that .oif files have a file and associated folder of files
# with the same name (eg. file1.oif and file1 folder)
    elif file.endswith('.oif'):
        code = int(np.random.choice(indices_array))
        results[file] = code
        os.rename(file, str(code) + ".oif")
        folder_name = file + '.oif.files'
        os.rename(folder_name, str(code) + '.oif.files')
        indices_array = indices_array[indices_array != code]

# Skip any folders associated with .oif files as they will be renamed in the
# above elif statement
    else:
        continue

# Place the dictionary containing the image original title and the associated
# code into a readable file
json.dump(results, open("codes.txt", 'w'), indent=2)
