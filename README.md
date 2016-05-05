# NIXus

**NIXus** a docker powerered next generation *application server* kind.

Application servers are typically coupled to ecosystems like .NET platform or JavaEE.
They are able to run just some kind of applications. In JavaEE, a server will run just JVM aplications deployed as WAR or EAR files.

*Docker* is a relatively new technology. It's an *application container*.
It allows to run any contenerized application without having to install all the required runtime in the host machine.

**NIXus** is basically a group of microservices containers that run in choreography.

> Basically it can run anything.

# Usage

Install [Docker Toolbox](https://www.docker.com/products/docker-toolbox) and configure docker.

Clone this repository:
```
$ git clone https://github.com/aitoroses/nixus
```

Configure a domain name into `env.sh` ( *dev.docker*  by default ), needed by the proxy.

Get **NIXus** running:

```
$ ./start.sh
```

Run a hello world container two times:
```
$ docker run -it -p :8000 jwilder/whoami
$ docker run -it -p :8000 jwilder/whoami

```

Try to do a CURL:
```
$ curl -L http://dev.docker/whoami

$ curl -L http://dev.docker:8000
```

Will return the container ID of the one that responds.
```
I'm c1b218dd8881
```

If you setup your DNS to resolve `whoami.dev.docker` you can also do
```
curl -L http://whoami.dev.docker
```

Thats all, your hello-world container is running with service discovery and clusterized.


# How does it work?

![](./docs/graffle.jpg)

NIXus registers when a new container has started/stoped 
and then it creates the correspoinding configuration files and stores the required container information.

# Service Autodiscovery

The **proxy** and **autodiscovery** containers magically are able to map a route to a container.
They just start a proxy server that is able to map a subdomain or a path to an specific container IP and Port.
This is done automatically.

For example, just by doing `docker run -it -p :8000 hello` the hello image will run as a container.

The port `tcp/8000` will be mapped to an arbitrary port in the host `tcp/8000 -> tcp/31892`.

NIXus will recognize that information and make the container discoverable through:

* `http://domain.com:8000`
* `http://domain.com/hello`
* `http://hello.domain.com`

---


 
You can also access container discovery data that exists in etcd:

```
curl -L http://dev.docker:4001/v2/keys/backends/whoami

{
   "action":"get",
   "node":{
      "key":"/backends/whoami",
      "dir":true,
      "nodes":[
         {
            "key":"/backends/whoami/a8e9c116f15e",
            "value":"192.168.99.100:32770",
            "expiration":"2016-05-05T16:09:41.982813865Z",
            "ttl":12,
            "modifiedIndex":2547,
            "createdIndex":2547
         },
         {
            "key":"/backends/whoami/port",
            "value":"8000",
            "expiration":"2016-05-05T16:09:41.984601416Z",
            "ttl":12,
            "modifiedIndex":2550,
            "createdIndex":2550
         },
         {
            "key":"/backends/whoami/c1b218dd8881",
            "value":"192.168.99.100:32771",
            "expiration":"2016-05-05T16:09:41.984006361Z",
            "ttl":12,
            "modifiedIndex":2549,
            "createdIndex":2549
         }
      ],
      "modifiedIndex":4,
      "createdIndex":4
   }
}
```



---

# Clusterization

Other interesting property is that the proxy can replicate and load balance those containers across different hosts, 
so that each container is clusterizable on itself.

Like in the example above, we can just do:

* `docker run -it -p :8000 --name hello-1 hello`
* `docker run -it -p :8000 --name hello-2 hello`
* `docker run -it -p :8000 --name hello-2 hello`

The same container will be spawned 3 times and NIXus will handle load balancing by default.

# License

Licensed under the MIT license. 2016 aitor.oses@gmail.com