ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ENV HOME=/home/docker_user

COPY scripts ${HOME}/scripts

RUN chmod +x ${HOME}/scripts/*.sh

# Install OpenCV
ARG OPENCV_VERSION=4.4.0

RUN ${HOME}/scripts/opencv_install_deps.sh
RUN ${HOME}/scripts/opencv_install.sh ${OPENCV_VERSION}