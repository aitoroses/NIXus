FROM golang:1.6.2-alpine
RUN apk add --no-cache git

RUN mkdir -p $GOPATH/src/docker-rest
ADD ./ $GOPATH/src/docker-rest
RUN go get github.com/tools/godep
RUN cd $GOPATH/src/docker-rest && godep restore

WORKDIR $GOPATH/src/docker-rest

EXPOSE 12053
EXPOSE 12054

CMD go run main.go -p :12053
