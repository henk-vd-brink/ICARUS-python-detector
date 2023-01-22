#!/bin/bash

OPENCV_VERSION=$1
MAKE_FLAGS=-j$(nproc)

cd /tmp

git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv.git

mkdir /tmp/opencv/build
cd /tmp/opencv/build

cmake  \
    -D CPACK_BINARY_DEB=ON \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
    -D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
    -D BUILD_opencv_java=OFF \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
    -D WITH_EIGEN=ON \
    -D ENABLE_NEON=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D WITH_GSTREAMER=ON \
    -D WITH_LIBV4L=ON \
    -D WITH_OPENGL=ON \
    -D WITH_OPENCL=OFF \
    -D WITH_IPP=OFF \
    -D WITH_TBB=ON \
    -D WITH_QT=OFf \
    -D BUILD_TIFF=ON \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_TESTS=OFF \
    .. \

make ${MAKE_FLAGS}

make install

rm -rf /tmp/opencv*