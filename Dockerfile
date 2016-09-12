FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y wget
RUN wget -O /etc/apt/sources.list.d/neurodebian.sources.list http://neuro.debian.net/lists/xenial.us-ca.full
RUN apt-key adv --recv-keys --keyserver hkp://pgp.mit.edu:80 0xA5D32F012649A5A9

# Run apt-get calls
RUN apt-get update \
    && apt-get install -y python-mvpa2

RUN mkdir -p /code
COPY run.py /code/run.py

COPY version /version

ENTRYPOINT ["/code/run.py"]
