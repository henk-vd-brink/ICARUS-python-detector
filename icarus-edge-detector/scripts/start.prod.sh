#!/bin/bash

FILE_NAME_PREFIX=$1

/usr/src/tensorrt/bin/trtexec \
    --fp16 \
    --workspace=2000 \
    --verbose \
    --buildOnly \
    --saveEngine=${PWD}/assets/${FILE_NAME_PREFIX}.trt \
    --onnx=${PWD}/assets/${FILE_NAME_PREFIX}.onnx # input

python3 -m src.detector.entrypoints.gstreamer_app