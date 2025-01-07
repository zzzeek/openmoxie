#!/bin/sh

echo "Building and pushing 'latest'"
echo docker-compose build
echo docker-compose push
export OPENMOXIE_VERSION=$(cat site/VERSION)
echo "Building and pushing '$OPENMOXIE_VERSION'"
echo docker-compose build
echo docker-compose push
