#!/usr/bin/env bash

set -e

DOCKER_REGISTRY="${DOCKER_REGISTRY:-eu.gcr.io/census-eq-ci}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
LOOKUP_URL="${LOOKUP_URL:-0.0.0.0:9000}"

helm tiller run \
    helm upgrade --install \
    address-lookup-api \
    k8s/helm \
    --set lookup_url=${LOOKUP_URL} \
    --set image.repository=${DOCKER_REGISTRY}/eq-address-lookup-api \
    --set image.tag=${IMAGE_TAG}
