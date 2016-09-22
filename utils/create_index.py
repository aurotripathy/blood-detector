#! /usr/bin/env python

import os
from random import shuffle

path = '/media/tempuser/RAID 5/blood-dataset/dl_images_flickr_01_320x240'
file_list = []
for root, dirs, files in os.walk(path):
    for f in files:
        # print '{}\n'.format(os.path.join(root, f))
        file_list.append(os.path.join(root, f))
shuffle(file_list)
for f in file_list: print '{}\n'.format(f) 
with open('flickr_index.txt', 'w') as f:
    for fl in file_list:
        f.write('{}\n'.format(fl))

        




    
