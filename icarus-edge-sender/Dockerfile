FROM python:3.9.15-slim-bullseye

ENV HOME=/home/docker_user

WORKDIR ${HOME}

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY requirements.txt ${HOME}/requirements.txt
RUN pip3 install -r ${HOME}/requirements.txt

COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src
