FROM prominendt/icarus:arm64v8-cuda102a53-py3.7-opencv4.4.0

ENV HOME=/home/docker_user

RUN apt-get update \
    && apt-get install -y \
        g++ \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        python3-dev

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

USER docker_user

WORKDIR ${HOME}

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src ${HOME}/src

