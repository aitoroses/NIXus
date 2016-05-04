#!/bin/bash

pm2 stop /etc/proxy.js
pm2 start /etc/proxy.js
