#!/usr/bin/env bash

set -euo pipefail

base_url="https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library"

kubectl apply -f "${base_url}/general/containerlimits/template.yaml"
kubectl apply -f "${base_url}/pod-security-policy/read-only-root-filesystem/template.yaml"
kubectl apply -f "${base_url}/pod-security-policy/users/template.yaml"

kubectl get constrainttemplates \
    k8scontainerlimits \
    k8spspreadonlyrootfilesystem \
    k8spspallowedusers
