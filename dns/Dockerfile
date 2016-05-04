FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y wget make gcc binutils python-pip python-dev libssl-dev libffi-dev bash curl

WORKDIR /root

RUN pip install python-etcd Jinja2

RUN curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
RUN apt-get install -y nodejs
RUN npm i -g pm2 redbird

ADD . /app

WORKDIR /app

CMD ["python", "main.py"]
