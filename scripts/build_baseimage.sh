#!/bin/bash

export $(grep -v '^#' .env.example | xargs)

BUILD_VERSION=$(date '+%Y-%m-%d')

docker buildx build \
    -t ${CONTAINER_REGISTRY}/icarus-edge-baseimage:${BUILD_VERSION:-latest} docker --push