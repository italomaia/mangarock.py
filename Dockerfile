FROM python:3.7-alpine

ENV USR nonroot
ENV HOME /home/${USR}

RUN apk add shadow && \
    groupadd -g 1000 -r ${USR} && \
    useradd -u 1000 -d ${HOME} -m -r -g ${USR} ${USR}

WORKDIR ${HOME}
COPY --chown=1000:1000 . ${HOME}/mangarock
RUN pip install ./mangarock &&\
    rm -rf ./mangarock