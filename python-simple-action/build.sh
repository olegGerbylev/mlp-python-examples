#!/bin/bash

ROOT=$(dirname $0)
cd "$ROOT"

BRANCH=$(echo $1 | tr '[:upper:]' '[:lower:]')
ACTION_NAME=simple-action-example
IMAGE=docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH

#./set_mlp_sdk_version.sh "$BRANCH"

docker build . -t "$IMAGE"

echo "$IMAGE"

docker push "$IMAGE"
