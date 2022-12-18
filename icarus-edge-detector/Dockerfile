FROM nvcr.io/nvidia/l4t-ml:r32.7.1-py3

ENV HOME=/home/docker_user

WORKDIR ${HOME}

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY requirements.txt ${HOME}/requirements.txt
RUN pip3 install -r ${HOME}/requirements.txt

COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src
COPY tests ${HOME}/tests

RUN pip3 install -e src/

COPY assets/ ${HOME}/assets/