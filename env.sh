#! /bin/bash

# export HOST_IP=$(hostname --all-ip-addresses | awk '{print $1}')
export HOST_IP=192.168.99.100
export ETCD_HOST=$HOST_IP:4001
