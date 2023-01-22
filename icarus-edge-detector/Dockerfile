ARG BASE_IMAGE

FROM ${BASE_IMAGE}

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_HOME="/usr/local/cuda"
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# Install PyCuda and Numba
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --verbose pycuda
RUN pip3 install --no-cache-dir --verbose numba

# Install Source Code
ENV HOME=/home/docker_user

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src
COPY tests ${HOME}/tests

RUN chown -R docker_user ${HOME}

USER docker_user

WORKDIR ${HOME}

RUN pip3 install -e src/

USER docker_user