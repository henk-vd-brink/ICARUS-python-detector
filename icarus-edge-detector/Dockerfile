ARG BASE_IMAGE=cricarusprod001.azurecr.io/icarus-edge-l4t-base:r32.7.1

FROM ${BASE_IMAGE}

WORKDIR ${HOME}

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY requirements.txt ${HOME}/requirements.txt
RUN pip install -r ${HOME}/requirements.txt

COPY assets ${HOME}/assets
COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src



