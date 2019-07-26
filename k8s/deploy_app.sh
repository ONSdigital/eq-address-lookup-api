#!/usr/bin/env bash

set -e

if [[ -z "$1" ]]; then
  echo "LOOKUP_URL is mandatory"
  exit 1
fi

LOOKUP_URL=$1
DOCKER_REGISTRY="${2:-eu.gcr.io/census-eq-ci}"
IMAGE_TAG="${3:-pricem_v16}"

helm tiller run \
    helm upgrade --install \
    address-lookup-api \
    k8s/helm \
    --set lookup_url=${LOOKUP_URL} \
    --set image.repository=${DOCKER_REGISTRY}/eq-address-lookup-api \
    --set image.tag=${IMAGE_TAG}
