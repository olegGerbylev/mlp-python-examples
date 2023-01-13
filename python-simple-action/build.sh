#!/bin/bash

ROOT=$(dirname $0)
cd $ROOT

ACTION_NAME=gate-python-action1
BRANCH=$(git rev-parse --abbrev-ref HEAD)

IMAGE=docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH
DOCKER_BUILDKIT=1 docker build . --ssh default -t $IMAGE

echo $IMAGE

#docker push $IMAGE

