#! /bin/bash

for config_file in `find . -name train_infer_python.txt`; do
    bash prepare.sh $config_file 'lite_train_lite_infer';
    bash test_train_inference_python.sh $config_file 'lite_train_lite_infer';
done