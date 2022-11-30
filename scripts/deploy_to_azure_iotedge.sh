#!/bin/bash

export BUILD_VERSION=$1
export DEPLOYMENT_VERSION=$2

export AZ_IOTHUB_NAME="iot-icarus-prod-westeu-001"
export AZ_TMP_DEPLOYMENT_FILE_PATH="/tmp/deployment_${DEPLOYMENT_VERSION}.json"

python3 scripts/python/build_deployment_manifest.py

az iot edge deployment create \
    -d ${DEPLOYMENT_VERSION} \
    -n ${AZ_IOTHUB_NAME} \
    --content ${AZ_TMP_DEPLOYMENT_FILE_PATH} \
    --target-condition "deviceId='jetsonnano0" \
    --priority 100