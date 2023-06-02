#!/bin/bash

BRANCH=$(echo $1 | tr '[:upper:]' '[:lower:]')

MLP_SDK_HAS_PARALLEL_BRANCH=$(git ls-remote --heads git@gitlab.just-ai.com:ml-platform-pub/mlp-python-sdk.git "$BRANCH" | wc -l)

if [ "$MLP_SDK_HAS_PARALLEL_BRANCH" -eq '1' ]
then
  MLP_SDK_VERSION=${BRANCH}
else
  MLP_SDK_VERSION=dev
fi

sed -i "s/git+https:\\/\\/git@gitlab.just-ai.com\\/ml-platform-pub\\/mlp-python-sdk.git@dev/git+https:\\/\\/git@gitlab.just-ai.com\\/ml-platform-pub\\/mlp-python-sdk.git@${MLP_SDK_VERSION}/" requirements.txt