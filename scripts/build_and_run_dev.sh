#!/bin/bash

docker-compose -f docker-compose.build.yaml build

docker run -it \
    --privileged \
    --network host \
    -v /home/jetson/repos/ICARUS-python-detector/icarus-edge-detector/src/:/home/docker_user/src \
    -v /home/jetson/repos/ICARUS-python-detector/icarus-edge-detector/assets/:/home/docker_user/assets \
    cricarusprod001.azurecr.io/icarus-edge-detector bash