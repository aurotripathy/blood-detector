**Installation**

Clone the repo in the examples directory of Caffe. It must be as the same level at the rest of the examples.

**Test the detector against the model**

`./bld_conf_mat_classifier.py -d googlenet/deploy.prototxt -m snapshots_bvlc_googlenet/bvlc_googlenet_iter_80000.caffemodel -l val_label.txt`

