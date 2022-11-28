#!/bin/bash

BUILD_VERSION="$(date +%Y%m%d-%H%M)"
DEPLOYMENT_VERSION="dev-$BUILD_VERSION"

./scripts/build_and_push.sh $BUILD_VERSION

./scripts/deploy_to_iotedge.sh $BUILD_VERSION $DEPLOYMENT_VERSION