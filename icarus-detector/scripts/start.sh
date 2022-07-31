#!/bin/bash

python3 -m scripts.tensorrt.build_tensorrt_engine \
    -o=/usr/docker_user/assets/yolov4.onnx \
    -e=/usr/docker_user/assets \
    -v \
    -w=3
