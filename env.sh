#! /bin/bash

export HOST_IP=$(docker-machine ip $(docker-machine active))
export ETCD_HOST=$HOST_IP:4001
