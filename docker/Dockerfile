ARG BASE_IMAGE

FROM ${BASE_IMAGE}

# Install OpenCV dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
	gfortran \
        cmake \
        git \
        file \
        tar \
        python3.8-dev \
        libatlas-base-dev \
        libavcodec-dev \
        libavformat-dev \
        libavresample-dev \
        libcanberra-gtk3-module \
        libdc1394-22-dev \
        libeigen3-dev \
        libglew-dev \
        libgstreamer-plugins-base1.0-dev \
        libgstreamer-plugins-good1.0-dev \
        libgstreamer1.0-dev \
        libgtk-3-dev \
        libjpeg-dev \
        libjpeg8-dev \
        libjpeg-turbo8-dev \
        liblapack-dev \
        liblapacke-dev \
        libopenblas-dev \
        libpng-dev \
        libpostproc-dev \
        libswscale-dev \
        libtbb-dev \
        libtbb2 \
        libtesseract-dev \
        libtiff-dev \
        libv4l-dev \
        libxine2-dev \
        libxvidcore-dev \
        libx264-dev \
        libgtkglext1 \
        libgtkglext1-dev \
        pkg-config \
        qv4l2 \
        v4l-utils \
        v4l2ucp \
        zlib1g-dev \
	curl \
	ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Clone OpenCV
ARG OPENCV_VERSION=4.4.0

WORKDIR /tmp

RUN git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv.git \
        && git clone --depth 1 --branch ${OPENCV_VERSION} https://github.com/opencv/opencv_contrib.git

# Build OpenCV
WORKDIR /tmp/opencv/build

RUN cmake  \
        -D CPACK_BINARY_DEB=ON \
        -D BUILD_EXAMPLES=OFF \
        -D BUILD_opencv_python2=OFF \
        -D BUILD_opencv_python3=ON \
        -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
        -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib/modules \
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
        ..

RUN make -j4

# Install OpenCV
RUN make install