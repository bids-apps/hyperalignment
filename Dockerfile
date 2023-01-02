FROM ubuntu:18.04

# Prepare environment
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                    apt-utils \
                    autoconf \
                    build-essential \
                    bzip2 \
                    ca-certificates \
                    curl \
                    git \
                    libtool \
                    lsb-release \
                    netbase \
                    pkg-config \
                    unzip \
                    xvfb && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV DEBIAN_FRONTEND="noninteractive" \
    LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# PyMVPA
RUN apt-get update && \
    apt-get install -y --no-install-recommends python2.7

RUN apt-get update && \
    mkdir /dev/fuse && \
    chmod 777 /dev/fuse && \
    apt-get install -y python-mvpa2 && \
    apt-get remove -f -y --purge fuse

RUN mkdir -p /code
COPY run.py /code/run.py

COPY version /version

ENTRYPOINT ["/code/run.py"]
