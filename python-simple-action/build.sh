#!/bin/bash

ROOT=$(dirname $0)
cd "$ROOT"

BRANCH=$(echo $1 | tr '[:upper:]' '[:lower:]')

./set_mlp_sdk_version.sh "$BRANCH"

ACTION_NAME=simple-action-example

eval $(ssh-agent)
ssh-add "$HOME"/.ssh/id_rsa
IMAGE=docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH
DOCKER_BUILDKIT=1 \
docker build . --ssh default -t "$IMAGE"

echo "$IMAGE"

docker push "$IMAGE"
