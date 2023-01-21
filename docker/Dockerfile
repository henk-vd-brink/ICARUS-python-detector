ARG BASE_IMAGE=nvcr.io/nvidia/l4t-tensorrt:r8.2.1-runtime

FROM --platform=linux/arm64/v8 ${BASE_IMAGE}

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_HOME="/usr/local/cuda"
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# Install PyCuda and Numba
RUN pip3 install --no-cache-dir --verbose pycuda
RUN pip3 install --no-cache-dir --verbose numba

# Copy scripts
COPY scripts /scripts
RUN chmod +x /scripts/*.sh

# Install OpenCV
ARG OPENCV_VERSION=4.4.0

RUN /scripts/opencv_install_deps.sh
RUN /scripts/opencv_install.sh ${OPENCV_VERSION}