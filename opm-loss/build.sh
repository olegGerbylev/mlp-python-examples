#!/bin/bash

ROOT=$(dirname $0)
cd "$ROOT"

IMAGE=docker-hub.just-ai.com/caila-actions/opm

docker build . -t "$IMAGE"

echo "$IMAGE"

docker push "$IMAGE"
