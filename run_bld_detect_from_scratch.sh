#!/bin/bash

TOOLS=../../build/tools

export HDF5_DISABLE_VERSION_CHECK=1
export PYTHONPATH=.
rm logs/bld_cnn_model.log
GLOG_logtostderr=1  $TOOLS/caffe train -solver net/bld_cnn_solver.prototxt 2>&1 | tee -a logs/bld_cnn_no_resize_model.log
echo "Done."
