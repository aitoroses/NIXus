FROM golang:1.6.2-alpine

RUN mkdir -p $GOPATH/src/docker-proxy-client
ADD ./ $GOPATH/src/docker-proxy-client

RUN cd $GOPATH/src/docker-proxy-client

WORKDIR $GOPATH/src/docker-proxy-client

EXPOSE 3000

CMD go run main.go
