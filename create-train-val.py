#!/usr/bin/env python

import fnmatch
import os
from random import shuffle
from sklearn.cross_validation import train_test_split

path = '/media/tempuser/RAID 5/blood-dataset'
NO_BLOOD_LABEL = 0
YS_BLOOD_LABEL = 1

extensions = ['*.JPG', '*.jpg', '*.png', '*.PNG', '*.JEPG', '*.jpeg']
img_files = []
for root, dirnames, filenames in os.walk(path):
    for extension in extensions:
        for filename in fnmatch.filter(filenames, extension):
            img_files.append(os.path.join(root, filename))

shuffle(img_files) # in-place

print "names of files,  {}".format(img_files)
print "number of files, {}".format(len(img_files))


def prep_labels(label_file, names_file):
    blood_label_count , no_blood_label_count = 0, 0
    with open(label_file, 'w') as f:
        for img_name in names_file:
            if '/NoBlood/' in img_name:
                f.write ("{} {}\n".format(img_name, NO_BLOOD_LABEL))
                no_blood_label_count += 1
            elif '/Blood/' in img_name:
                f.write ("{} {}\n".format(img_name, YS_BLOOD_LABEL))
                blood_label_count += 1
            else:
                print "Error in file path name"
                exit(2)
    return blood_label_count, no_blood_label_count

# 80/20 train/val split
img_train, img_val = train_test_split(img_files, test_size = 0.2)
print "Length of train data       {}".format(len(img_train))
print "Length of validation  data {}".format(len(img_val))
val_blood_label_count, val_no_blood_label_count = prep_labels('val_label.txt', img_val)
train_blood_label_count, train_no_blood_label_count = prep_labels('train_label.txt', img_train)
print "Training   set - count of images w/blood {} and w/o blood {}".format(train_blood_label_count, train_no_blood_label_count) 
print "Validation set - count of images w/blood {} and w/o blood {}".format(val_blood_label_count, val_no_blood_label_count) 
