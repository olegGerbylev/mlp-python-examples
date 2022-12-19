#!/bin/bash

ROOT=$(dirname $0)
cd $ROOT

ACTION_NAME=gate-python-action1
BRANCH=$(git rev-parse --abbrev-ref HEAD)

mkdir ./tmp-ssh
cp ~/.ssh/* ./tmp-ssh

export DOCKER_BUILDKIT=1
docker build .  \
           -t at

#echo docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH

#docker push docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH

