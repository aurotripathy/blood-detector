#!/usr/bin/env python

import numpy as np
import glob
from sklearn.metrics import confusion_matrix
from sklearn.metrics import average_precision_score, recall_score, accuracy_score, precision_score
import argparse
from pudb import set_trace

caffe_root = '../../'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe
caffe.set_mode_gpu()
caffe.set_device(0)


def get_args():
    parser = argparse.ArgumentParser(
        description='Classifies a single image. Ensure the image is resized beforehand.')
    # Add arguments
    parser.add_argument(
        '-d', '--deploy_network_def', type=str, help='the deploy network definition prototxt file', required=True)
    parser.add_argument(
        '-m', '--model', type=str, help='Model to run it on', required=True)
    parser.add_argument(
        '-i', '--image_file', type=str, help='image to be classified', required=True)

    args = parser.parse_args()
    d = args.deploy_network_def
    m = args.model
    i = args.image_file

    return d, m, i


deploy_network, trained_model, img_file = get_args()

net = caffe.Classifier(deploy_network, trained_model,
                       mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                       channel_swap=(2, 1, 0),
                       raw_scale=255,
                       image_dims=(320, 240))

input_image = caffe.io.load_image(img_file)
input_image = caffe.io.resize_image(input_image, (320, 240))
prediction = net.predict([input_image], oversample=False)
label_pred = prediction[0].argmax()
print "Probabilities {} label {}".format(prediction, label_pred)
