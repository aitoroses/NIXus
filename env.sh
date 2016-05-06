#! /bin/bash

export HOST_IP=$(docker-machine ip)
export ETCD_HOST=$HOST_IP:4001
