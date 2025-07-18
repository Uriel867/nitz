FROM python:3.13-alpine3.22 AS base

# copy installation files
COPY requirements.txt /tmp/requirements.txt

USER root

RUN python3 -m pip install -r /tmp/requirements.txt --break-system-packages && rm /tmp/requirements.txt

WORKDIR /workspace
# copy service files
COPY src /workspace/src/

WORKDIR /workspace/src
