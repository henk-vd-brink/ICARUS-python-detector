#!/bin/bash

FILE_NAME_PREFIX=$1

FILE="${PWD}/assets/${FILE_NAME_PREFIX}.trt"
if [ -f "${FILE}" ];
    then
        echo "${FILE} exists."
else
    echo "${FILE} does not exist, starting TensorRT engine"
    /usr/src/tensorrt/bin/trtexec \
    --fp16 \
    --workspace=2000 \
    --verbose \
    buildOnly \
    --saveEngine=${PWD}/assets/${FILE_NAME_PREFIX}.trt \
    --onnx=${PWD}/assets/${FILE_NAME_PREFIX}.onnx # input
fi

python3 -m src.detector.entrypoints.gstreamer_app