#!/bin/bash
set -e

BUILDER_IMG=freetechsolutions/omlapp-builder:latest

PACKAGE_VERSION=$(cat ../../.omnileads_version)
docker login -u $DOCKER_USER -p $DOCKER_PASSWORD

case $CI_COMMIT_REF_NAME in
  master)
    docker build -f Dockerfile --build-arg BUILDER_IMG=$BUILDER_IMG -t freetechsolutions/omlapp:latest ../..
    docker push freetechsolutions/omlapp:latest
    ;;
  *)
    docker build -f Dockerfile --build-arg BUILDER_IMG=$BUILDER_IMG -t freetechsolutions/omlapp:$PACKAGE_VERSION ../..
    docker push freetechsolutions/omlapp:$PACKAGE_VERSION
    ;;
esac
