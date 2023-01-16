#!/bin/bash

docker-compose \
    --file docker-compose.ci.build.yaml \
    --env-file .env.example \
    build icarus-edge-detector

docker-compose \
    --env-file .env.example \
    up