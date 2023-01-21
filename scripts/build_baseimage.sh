#!/bin/bash

export $(grep -v '^#' .env.example | xargs)

docker buildx build -t ${CONTAINER_REGISTRY}/icarus-edge-baseimage:${BUILD_VERSION:-latest} docker