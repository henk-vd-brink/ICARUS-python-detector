#!/bin/bash

export $(grep -v '^#' .env.example | xargs)

BUILD_VERSION=$(date '+%Y-%m-%d')

docker buildx build \
    --tag ${CONTAINER_REGISTRY}/icarus-edge-baseimage:${BUILD_VERSION:-latest} docker --push