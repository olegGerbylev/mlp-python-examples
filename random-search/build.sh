#!/bin/bash

ROOT=$(dirname $0)
cd $ROOT

SERVICE_NAME=mlp-random-search
BUILD_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BRANCH_NAME_LOWER=`echo $BUILD_BRANCH | tr '[:upper:]' '[:lower:]'`

IMAGE=docker-hub.just-ai.com/caila-actions/$SERVICE_NAME:$BRANCH_NAME_LOWER

mvn clean package
#export DOCKER_BUILDKIT=1
docker build . -t $IMAGE
docker push $IMAGE



