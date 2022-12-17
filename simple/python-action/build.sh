#!/bin/bash
NEXUS_USER=$1
NEXUS_PASS=$2

ACTION_NAME=gate-python-action
BUILD=$3
BRANCH=$4
BRANCH2=$5

MAJOR_VERSION=1
MINOR_VERSION=0
if ! [[ "$BRANCH2" =~ ^(master|dev|release)$ ]];
then
  MINOR_VERSION=$MINOR_VERSION+$BRANCH2;
fi

rm -f caila_transport-*.whl
pip3 download caila-transport==$MAJOR_VERSION.$MINOR_VERSION.$BUILD --no-deps --index-url=https://$NEXUS_USER:$NEXUS_PASS@nexus.just-ai.com/repository/pypi-hosted/simple
docker build . -t docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH

docker tag docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH docker-hub.just-ai.com/caila-actions/$ACTION_NAME:$BRANCH-$BUILD

