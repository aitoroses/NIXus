FROM ubuntu:14.04
MAINTAINER Jason Wilder <jason@influxdb.com>

RUN apt-get update -y
RUN apt-get install -y wget python python-pip python-dev libssl-dev libffi-dev bash

RUN mkdir /app
WORKDIR /app

RUN wget https://github.com/jwilder/docker-gen/releases/download/0.7.1/docker-gen-linux-amd64-0.7.1.tar.gz
RUN tar xvzf docker-gen-linux-amd64-0.7.1.tar.gz -C /usr/local/bin

RUN pip install python-etcd

ADD . /app

ENV DOCKER_HOST unix:///var/run/docker.sock

CMD docker-gen -interval 10 -watch -notify "python /tmp/register.py" etcd.tmpl /tmp/register.py
