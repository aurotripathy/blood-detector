#!/bin/bash

TOOLS=../../build/tools

export HDF5_DISABLE_VERSION_CHECK=1
export PYTHONPATH=.

# weight from alexnet
# GLOG_logtostderr=1  $TOOLS/caffe train -solver net/bld_cnn_solver.prototxt -weights /media/tempuser/RAID\ 5/caffe-test/caffe/models/bvlc_alexnet/bvlc_alexnet.caffemodel \
#                                        2>&1 | tee -a logs/bld_cnn_no_resize_model.log

# weight from caffenet
GLOG_logtostderr=1  $TOOLS/caffe train -solver net/bld_cnn_solver.prototxt -weights /media/tempuser/RAID\ 5/caffe-test/caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel \
                                       2>&1 | tee -a logs/bld_cnn_no_resize_model.log


echo "Done."

