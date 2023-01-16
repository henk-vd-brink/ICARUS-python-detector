FROM nvcr.io/nvidia/l4t-tensorrt:r8.2.1-runtime

COPY scripts /tmp/scripts

# Install OpenCV
ARG OPENCV_URL=https://nvidia.box.com/shared/static/5v89u6g5rb62fpz4lh0rz531ajo2t5ef.gz
ARG OPENCV_DEB=OpenCV-4.5.0-aarch64.tar.gz

RUN chmod +x /tmp/scripts \
        && /tmp/scripts/opencv_install.sh ${OPENCV_URL} ${OPENCV_DEB}