#! /usr/bin/env python

'''
Typical use will be...
./create_index.py -d /media/tempuser/RAID 5/blood-dataset/dl_images_flickr_01_320x240 -f flickr_index.txt
'''

import os
from random import shuffle
from argparse import ArgumentParser

def get_parameters():
    parser = ArgumentParser()
    parser.add_argument("-d", "--dir", dest="dir_path",
                         help="The path where the images resides", required=True)
    parser.add_argument("-f", "--index_file", dest="index_file",
                         help=" with files to be tested agaist the model", required=True)
    args = parser.parse_args()
    return args.dir_path, args.index_file


dir_path, index_file = get_parameters()
file_list = []
for root, dirs, files in os.walk(dir_path):
    for f in files:
        file_list.append(os.path.join(root, f))
shuffle(file_list)
for f in file_list: print '{}\n'.format(f) 
with open(index_file, 'w') as f:
    for fl in file_list:
        f.write('{}\n'.format(fl))

        



    
