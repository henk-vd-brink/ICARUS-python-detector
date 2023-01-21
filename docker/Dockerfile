ARG BASE_IMAGE=nvcr.io/nvidia/l4t-tensorrt:r8.2.1-runtime

FROM --platform=linux/arm64/v8 ${BASE_IMAGE}

ENV HOME=/home/docker_user

COPY scripts ${HOME}/scripts

RUN chmod +x ${HOME}/scripts/*.sh

# Install OpenCV
ARG OPENCV_VERSION=4.4.0

RUN ${HOME}/scripts/opencv_install_deps.sh
RUN ${HOME}/scripts/opencv_install.sh ${OPENCV_VERSION}