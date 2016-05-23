from flask import Flask, jsonify

import etcd
import os
import sys


app = Flask(__name__)

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


@app.route('/')
def hello_world():
    try:
        return jsonify(get_services())
    except:
        print "Unexpected error:", sys.exc_info()[0]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
