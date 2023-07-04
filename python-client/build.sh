#!/bin/bash

ROOT=$(dirname $0)
cd "$ROOT"

BRANCH=$(echo $1 | tr '[:upper:]' '[:lower:]')
ACTION_NAME=client-app-example
IMAGE=docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH

./set_mlp_sdk_version.sh "$BRANCH"

DOCKER_BUILDKIT=1 docker build . -t "$IMAGE"

echo "$IMAGE"

docker push "$IMAGE"
