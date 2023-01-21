#!/bin/bash

export $(grep -v '^#' .env.example | xargs)

docker push ${CONTAINER_REGISTRY}/icarus-edge-baseimage:${BUILD_VERSION:-latest}