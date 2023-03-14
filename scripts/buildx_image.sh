#!/bin/bash

export $(grep -v '^#' .env.example | xargs)

BUILD_VERSION=$(date '+%Y-%m-%d')
export BASE_IMAGE=cricarusdev.azurecr.io/icarus-edge-baseimage:2023-01-22


docker buildx build \
    --tag cricarusdev.azurecr.io/icarus-edge-detector:${BUILD_VERSION:-latest} -f icarus-edge-detector/Dockerfile.prod --build-arg BASE_IMAGE=${BASE_IMAGE} icarus-edge-detector --push
