#!/usr/bin/env bash
# Demo script: create a temporary kind cluster, apply namespace, verify, and cleanup
set -euo pipefail

CLUSTER_NAME=nas-demo
NAMESPACE=integration-ns

echo "Creating kind cluster: $CLUSTER_NAME"
kind create cluster --name "$CLUSTER_NAME"

KUBECONFIG_PATH=$(kind get kubeconfig-path --name="$CLUSTER_NAME")
export KUBECONFIG="$KUBECONFIG_PATH"

echo "Using KUBECONFIG=$KUBECONFIG"

echo "Applying namespace via nas CLI"
./bin/nas create "$NAMESPACE" --apply --cpu-request 500m --memory-limit 1Gi

echo "Resources in cluster:"
kubectl get ns
kubectl -n "$NAMESPACE" get resourcequota,limitrange || true

echo "Cleaning up: deleting kind cluster $CLUSTER_NAME"
kind delete cluster --name "$CLUSTER_NAME"

echo "Demo complete"
