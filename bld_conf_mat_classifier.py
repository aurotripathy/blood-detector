#!/usr/bin/env python
# derived from http://www.cc.gatech.edu/~zk15/deep_learning/classify_test.py
import os
import numpy as np
import glob
from sklearn.metrics import confusion_matrix
from sklearn.metrics import average_precision_score, recall_score, accuracy_score, precision_score
import argparse
from pudb import set_trace
from shutil import copyfile, rmtree

caffe_root = '../../'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
caffe.set_mode_cpu()
caffe.set_device(0)

YS_BLOOD = 1
NO_BLOOD = 0

def pretty_print_conf_mat(mat):
    print '{:^30}'.format('Metrics from sklearm.metrics')
    print('')
    print('')
    print '{:^30}'.format('CONFUSION MATRIX')
    print '{:^30}'.format('----------------')
    print '{:10} {:10} {:10}'.format(' ', "pred '0'", "pred '1'")
    print '{:10} {:10} {:10}'.format(' ', '--------', '--------')
    print '{:10} {:<10} {:<10}'.format("GT '0'", mat[0][0], mat[0][1])
    print '{:10} {:<10} {:<10}'.format("GT '1'", mat[1][0], mat[1][1])
    print('')
    print('')
    return


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate the confusion matrix on the test data.')
    # Add arguments
    parser.add_argument(
        '-d', '--deploy_network_def', type=str, help='the deploy network definition prototxt file', required=True)
    parser.add_argument(
        '-m', '--model', type=str, help='Model to run it on', required=True)
    parser.add_argument(
        '-l', '--label_file', type=str, help='input dir', required=True)

    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    d = args.deploy_network_def
    m = args.model
    l = args.label_file

    return d, m, l


# Need three parameters, network definition, model, label file
deploy_network, trained_model, label_file = get_args()

# set_trace()

with open(label_file) as f:
    file_label_tuples = f.readlines()

images = [frame.rsplit(' ', 1)[0] for frame in file_label_tuples]
labels = [frame.rsplit(' ', 1)[1] for frame in file_label_tuples]
labels_gt = map(int, labels)

net = caffe.Classifier(deploy_network, trained_model,
                       mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                       channel_swap=(2, 1, 0),
                       raw_scale=255,
                       image_dims=(320, 240))

conf_matrix = np.zeros((2, 2), dtype=int)

dir_blood_as_no_blood = 'blood-as-no-blood/'
dir_no_blood_as_blood = 'no-blood-as-blood/'

if os.path.isdir(dir_blood_as_no_blood):
    rmtree(dir_blood_as_no_blood)
os.makedirs(dir_blood_as_no_blood)

if os.path.isdir(dir_no_blood_as_blood):
    rmtree(dir_no_blood_as_blood)
os.mkdir(dir_no_blood_as_blood)

labels_pred = []
for i, f in enumerate(images):
    input_image = caffe.io.load_image(f)
    input_image = caffe.io.resize_image(input_image, (320, 240))
    prediction = net.predict([input_image], oversample=False)
    label_pred = prediction[0].argmax()
    labels_pred.append(label_pred)

    if label_pred != labels_gt[i]:
        print('GT', labels_gt[i], 'pred', label_pred)
        # set_trace()
        if labels_gt[i] == YS_BLOOD and label_pred == NO_BLOOD:
            copyfile(f,  dir_blood_as_no_blood + os.path.basename(f))
        elif labels_gt[i] == NO_BLOOD and label_pred == YS_BLOOD:
            copyfile(f,  dir_no_blood_as_blood + os.path.basename(f))
      
# http://scikit-learn.org/stable/modules/classes.html#classification-metrics 
conf_matrix = confusion_matrix(labels_gt, labels_pred, labels=[0,1])
pretty_print_conf_mat(conf_matrix)
print('Average precision score', average_precision_score(labels_gt, labels_pred))
print('Precision score', precision_score(labels_gt, labels_pred))
print('Recall score', recall_score(labels_gt, labels_pred))
print('Accuracy score', accuracy_score(labels_gt, labels_pred))
print('Total images classified', len(images))
print('mean', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1))
