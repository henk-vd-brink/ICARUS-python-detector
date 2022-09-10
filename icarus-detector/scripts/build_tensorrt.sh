#!/bin/bash

python3 /home/docker_user/scripts/tensorrt/build_tensorrt_engine.py \
    -o=/home/docker_user/assets/yolov4.onnx \
    -e=/home/docker_user/assets \
    -v \
    -w=3 