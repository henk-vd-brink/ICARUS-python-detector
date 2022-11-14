#!/bin/bash

docker-compose -f docker-compose.build.yaml build icarus-edge-detector

docker run -it \
    --privileged \
    --network host \
    -v ${PWD}/icarus-edge-detector/src/:/home/docker_user/src \
    -v ${PWD}/icarus-edge-detector/assets/:/home/docker_user/assets \
    cricarusprod001.azurecr.io/icarus-edge-detector bash