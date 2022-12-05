FROM python:3.9.15-slim-bullseye

ENV HOME=/home/docker_user

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0

WORKDIR ${HOME}

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY requirements.txt ${HOME}/requirements.txt
RUN pip3 install -r ${HOME}/requirements.txt

COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src
