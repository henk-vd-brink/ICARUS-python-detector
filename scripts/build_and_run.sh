#!/bin/bash

export BUILD_ENVIRONMENT=$1

docker-compose \
    --file docker-compose.ci.build.yaml \
    --env-file .env.example \
    build icarus-edge-detector

docker-compose \
    --env-file .env.example \
    up