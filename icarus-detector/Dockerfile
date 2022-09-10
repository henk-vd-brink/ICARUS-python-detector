FROM test
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
RUN pip install pycuda

RUN useradd -m docker_user \
	&& usermod -a -G video docker_user

COPY requirements.txt ${HOME}/requirements.txt
RUN pip install -r ${HOME}/requirements.txt

COPY assets ${HOME}/assets
COPY scripts ${HOME}/scripts
RUN chmod +x ${HOME}/scripts/*.sh

COPY src ${HOME}/src



