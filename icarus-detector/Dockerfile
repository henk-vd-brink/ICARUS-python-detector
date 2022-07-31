FROM nvcr.io/nvidia/l4t-tensorrt:r8.2.1-runtime

ENV HOME=/usr/docker_user
ENV CPLUS_INCLUDE_PATH="${CPLUS_INCLUDE_PATH}:/usr/include/python3.6m/"

WORKDIR ${HOME}

RUN apt-get update \
    && apt-get install -y \
        g++ \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        python3-dev

RUN pip install --upgrade pip

COPY requirements.txt ${HOME}

COPY scripts ${HOME}/scripts

COPY assets ${HOME}/assets

# ENTRYPOINT ["python", "-m", "scripts.tensorrt.build_tensorrt_engine", "--onnx=assets/yolov4.onnx"]

# COPY requirements.txt ${HOME}

# RUN pip3 install -r requirements.txt
