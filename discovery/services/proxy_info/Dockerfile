FROM ubuntu:14.04

RUN apt-get update -y
RUN apt-get install -y wget make gcc binutils python-pip python-dev libssl-dev libffi-dev bash

RUN pip install python-etcd Jinja2 flask

COPY main.py /app/main.py

WORKDIR /app

EXPOSE 5000

CMD ["python", "main.py"]
