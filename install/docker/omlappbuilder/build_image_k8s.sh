#!/bin/bash

set -e
set -u
set -o pipefail

cd "$(dirname "$0")"

cp -a ../../../requirements/ .

docker build ${NO_CACHE:---no-cache} -t k8soml/omlapp-builder:k8s .

echo "To push docker image, run:"
echo "    docker push k8soml/omlapp-builder:k8s"
