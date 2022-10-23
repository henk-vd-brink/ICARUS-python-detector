#!/bin/bash

docker-compose -f docker-compose.build.yaml build icarus-base-image
docker-compose -f docker-compose.build.yaml build icarus-tensorflow-image
docker-compose -f docker-compose.build.yaml build icarus-pytorch-image

docker-compose -f docker-compose.build.yaml build icarus-edge-detector

docker-compose -f docker-compose.build.yaml push