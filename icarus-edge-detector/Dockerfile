ARG BASE_IMAGE

FROM ${BASE_IMAGE}

ENV HOME=/home/docker_user

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY requirements.txt ${HOME}/requirements.txt
RUN pip3 install -r ${HOME}/requirements.txt

COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src
COPY tests ${HOME}/tests

WORKDIR ${HOME}

RUN pip3 install -e src/

RUN chown -R docker_user ${HOME}

USER docker_user