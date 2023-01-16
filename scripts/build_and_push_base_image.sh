#!/bin/bash

docker-compose \
    --file docker-compose.ci.build.yaml \
    --env-file .env.example \
    build icarus-edge-baseimage

docker-compose \
    --file docker-compose.ci.build.yaml \
    --env-file .env.example \
    push icarus-edge-baseimage