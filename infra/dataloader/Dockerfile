FROM alpine:3.22.1 AS base

# installing curl for the http call
RUN apk update && apk add curl

# copy the loader script
WORKDIR /workspace
COPY loader.sh /workspace/loader.sh
