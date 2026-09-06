#!/usr/bin/env bash

set -Eeuo pipefail

INGRESS_NGINX_VERSION="controller-v1.15.1"
MANIFEST_URL="https://raw.githubusercontent.com/kubernetes/ingress-nginx/${INGRESS_NGINX_VERSION}/deploy/static/provider/baremetal/deploy.yaml"

echo "Installing ingress-nginx ${INGRESS_NGINX_VERSION} for a bare-metal cluster"
kubectl apply -f "${MANIFEST_URL}"

echo "Waiting for the ingress controller"
kubectl --namespace ingress-nginx rollout status \
    deployment/ingress-nginx-controller \
    --timeout=300s

echo "Assigning predictable NodePorts"
kubectl --namespace ingress-nginx patch service ingress-nginx-controller \
    --type=merge \
    --patch '{"spec":{"ports":[{"name":"http","port":80,"protocol":"TCP","targetPort":"http","nodePort":30080},{"name":"https","port":443,"protocol":"TCP","targetPort":"https","nodePort":30443}]}}'

kubectl --namespace ingress-nginx get pods -o wide
kubectl --namespace ingress-nginx get service ingress-nginx-controller
