#! /bin/bash

source ./env.sh

build() {
    docker-compose build
}

start() {
    docker-compose up -d
} 

logs() {
    docker-compose logs
}

stop() {
    docker-compose stop
}


case "$1" in
        start)
            start
            ;;
         
        stop)
            stop
            ;;
         
        build)
            status build
            ;;
        restart)
            stop
            start
            ;;
         
        *)
            echo $"Usage: $0 {start|stop|restart|build}"
            exit 1
 
esac