#!/usr/bin/python

import etcd
from jinja2 import Environment, PackageLoader
import os
from subprocess import call
import signal
import sys
import time

env = Environment(loader=PackageLoader('haproxy', 'templates'))
POLL_TIMEOUT=5

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

def get_etcd_addr():
    if "ETCD_HOST" not in os.environ:
        print "ETCD_HOST not set"
        sys.exit(1)

    etcd_host = os.environ["ETCD_HOST"]
    if not etcd_host:
        print "ETCD_HOST not set"
        sys.exit(1)

    port = 4001
    host = etcd_host

    if ":" in etcd_host:
        host, port = etcd_host.split(":")

    return host, port

def get_services():

    host, port = get_etcd_addr()
    client = etcd.Client(host=host, port=int(port))
    
    backends = client.read('/backends', recursive = True)
    frontends = client.read('/frontends', recursive = True)

    services = {}

    for i in frontends.children:
        service = i.key[1:].split("/")[1]
        services[service] = dict(backends={}, frontends=[])


    for i in backends.children:
        service = i.key[1:].split("/")[1]
        port = i.key[1:].split("/")[2]

        try:
            directive_rewrite_url = client.read('/directives/' + service + "/rewrite_url").value != "false"
        except:
            directive_rewrite_url = True

        endpoints = services[service]

        for b in i.children:
            try:
                container = i.key[1:].split("/")[3]
                endpoints["backends"][port] = []
                endpoints["backends"][port].append(dict(name=container, addr=i.value, rewrite=directive_rewrite_url))
            except:
                continue

    for i in frontends.children:
        service = i.key[1:].split("/")[1]
        endpoints = services[service]


        for b in i.children:
            try:
                context = b.key[1:].split("/")[2]
                endpoints["frontends"].append(dict(port=context, name=b.value))
            except:
                continue

    return services




def generate_config(services):
    template = env.get_template('haproxy.cfg.tmpl')
    with open("/etc/haproxy.cfg", "w") as f:
        f.write(template.render(services=services))

if __name__ == "__main__":
    current_services = {}
    while True:
        try:
            services = get_services()

            if not services or services == current_services:
                time.sleep(POLL_TIMEOUT)
                continue

            print "config changed. reload haproxy"
            generate_config(services)
            ret = call(["./reload-haproxy.sh"])
            if ret != 0:
                print "reloading haproxy returned: ", ret
                time.sleep(POLL_TIMEOUT)
                continue
            current_services = services

        except Exception, e:
            print "Error:", e

        time.sleep(POLL_TIMEOUT)