#!/bin/bash

ROOT=$(dirname $0)
cd $ROOT

ACTION_NAME=ak-fit-test-action
BUILD_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BRANCH_NAME_LOWER=`echo $BUILD_BRANCH | tr '[:upper:]' '[:lower:]'`

IMAGE=docker-hub.just-ai.com/caila-actions/$ACTION_NAME:sdktest-3

eval $(ssh-agent)
ssh-add $HOME/.ssh/id_rsa
export DOCKER_BUILDKIT=1
docker build . --ssh default -t $IMAGE