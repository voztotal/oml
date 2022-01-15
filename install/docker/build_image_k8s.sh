#!/bin/bash

set -e
set -u
set -o pipefail

cd "$(dirname "$0")"

BUILDER_IMG=k8soml/omlapp-builder:k8s

docker build ${NO_CACHE:---no-cache} -f Dockerfile --build-arg BUILDER_IMG=$BUILDER_IMG -t k8soml/omlapp:k8s ../..

echo "To push docker image, run:"
echo "    docker push k8soml/omlapp:k8s"
