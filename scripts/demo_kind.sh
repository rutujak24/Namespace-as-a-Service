#!/usr/bin/env bash
# Demo script: create a temporary kind cluster, apply namespace, verify, and cleanup
set -euo pipefail

CLUSTER_NAME=nas-demo
NAMESPACE=integration-ns

# Pre-flight checks: ensure required commands are installed
for cmd in kind kubectl docker; do
	if ! command -v "$cmd" >/dev/null 2>&1; then
		echo "Error: required command '$cmd' not found."
		case "$cmd" in
			kind)
				echo "Install kind (Linux):"
				echo "  curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64 && chmod +x ./kind && sudo mv ./kind /usr/local/bin/"
				echo "Or on macOS: brew install kind"
				;;
			kubectl)
				echo "Install kubectl (Linux):"
				echo "  curl -LO \"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\" && chmod +x kubectl && sudo mv kubectl /usr/local/bin/"
				echo "Or on macOS: brew install kubectl"
				;;
			docker)
				echo "Install Docker Desktop from https://www.docker.com/get-started or your OS package manager."
				;;
		esac
		exit 1
	fi
done

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
