#!/bin/bash

/usr/src/tensorrt/bin/trtexec \
    --onnx=/home/docker_user/assets/yolov4.onnx \
    --saveEngine=/home/docker_user/assets/yolov4.trt \
    --buildOnly \
    --fp16 \
    --verbose \
    --workspace=4096