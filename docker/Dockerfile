ARG BASE_IMAGE=nvcr.io/nvidia/l4t-tensorrt:r8.2.1-runtime

FROM --platform=linux/arm64/v8 ${BASE_IMAGE}

# Copy scripts
COPY scripts /scripts
RUN chmod +x /scripts/*.sh

# Install OpenCV
ARG OPENCV_VERSION=4.4.0

RUN /scripts/opencv_install_deps.sh
RUN /scripts/opencv_install.sh ${OPENCV_VERSION}