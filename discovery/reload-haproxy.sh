#!/bin/bash

/usr/local/sbin/haproxy -f /etc/haproxy.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)

# Rsyslog (Apparently needed for taking the config)
/etc/init.d/rsyslog restart
