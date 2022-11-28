#!/bin/bash

BUILD_VERSION_DEFAULT="$(date +%Y%m%d-%H%M)"
INPUT=$1

export BUILD_VERSION="${INPUT:-$BUILD_VERSION_DEFAULT}"

docker-compose -f docker-compose.ci.build.yaml build

while true; do
read -p "Do you want to proceed? (y/n)" yn

case $yn in
    [yY] ) break ;;
    [nN] ) exit;;
    * ) echo "Invalid response, try again.." exit ;;
esac
done

sudo -E docker-compose -f docker-compose.ci.build.yaml push

echo "Pushed images to cloud with tag: ${BUILD_VERSION}"