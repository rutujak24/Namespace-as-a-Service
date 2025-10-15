#!/usr/bin/env bash
# Example: create a namespace with kubectl
set -euo pipefail

NAME="$1"

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAME}
EOF

echo "Namespace ${NAME} created (or already exists)"
