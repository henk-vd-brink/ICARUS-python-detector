FROM cricarusprod001.azurecr.io/icarus-edge-baseimage

WORKDIR ${HOME}


RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY requirements.txt ${HOME}/requirements.txt
RUN pip install -r ${HOME}/requirements.txt

COPY assets ${HOME}/assets
COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src



