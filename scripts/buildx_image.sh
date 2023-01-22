#!/bin/bash

export $(grep -v '^#' .env.example | xargs)

BUILD_VERSION=$(date '+%Y-%m-%d')

docker buildx build \
    --file icarus-edge-detector/Dockerfile.prod \
    --tag ${CONTAINER_REGISTRY}/icarus-edge-detector:${BUILD_VERSION:-latest} \
    --build-arg BASE_IMAGE=${PROD_BASE_IMAGE} \
    icarus-edge-detector --push