# Namespace-as-a-Service — Details & Demo (Layman's)

What this project does (plain language)
--------------------------------------
- This project is a small command-line tool that helps create isolated spaces (namespaces) inside a Kubernetes cluster for teams or projects.
- When you ask the tool to "create" a namespace, it prepares three things:
  1. A Namespace object (the container for resources),
  2. A ResourceQuota object that caps how much CPU and memory workloads in the namespace can request/consume, and
  3. A LimitRange object that provides default CPU/memory requests and limits for containers in the namespace.
- You can preview what will be created (dry-run), or actually apply it to a cluster (with `--apply`).

Why this is useful
-------------------
- Teams can self-service namespaces with reasonable defaults and guardrails (quotas/limits). That prevents a single team from accidentally consuming all cluster resources.

Quick demo / test steps (what I ran locally)
-------------------------------------------
Prerequisites
- Docker running
- kind installed
- kubectl installed
- Python 3.9+ and venv support

1) Create and activate a Python virtualenv (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Start a local cluster with kind (the demo script does this):

```bash
kind create cluster --name nas-demo
# If your kind version doesn't support the '--name' flag for get kubeconfig,
# use the fallback: kind get kubeconfig > /tmp/nas-demo-kubeconfig
kind get kubeconfig --name nas-demo > /tmp/nas-demo-kubeconfig
export KUBECONFIG=/tmp/nas-demo-kubeconfig
kubectl cluster-info --context kind-nas-demo
kubectl get nodes
```

3) Fix permission error (if you hit it):

If you saw "bash: ./bin/nas: Permission denied" when running the CLI, make the CLI executable:

```bash
chmod +x bin/nas
```

4) Apply the namespace via the CLI (the command used in the demo):

```bash
./bin/nas create integration-ns --apply --cpu-request 500m --memory-limit 1Gi
```

Expected immediate outcome:
- The CLI should report a result with status `applied` (or show an error if something failed). The k8s wrapper writes YAML to a temp file and calls the Kubernetes API.

5) Inspect created resources:

```bash
kubectl get ns
kubectl -n integration-ns get resourcequota,limitrange
```

Expected output (approx):
- `kubectl get ns` will show `integration-ns` in the list.
- `kubectl -n integration-ns get resourcequota,limitrange` should show 1 ResourceQuota and 1 LimitRange in that namespace.

6) Cleanup (delete the kind cluster)

```bash
kind delete cluster --name nas-demo
rm /tmp/nas-demo-kubeconfig
```

Notes, troubleshooting and variations
------------------------------------
- If `kind get kubeconfig --name nas-demo` fails (different kind version), use `kind get kubeconfig > /tmp/nas-demo-kubeconfig` then set `KUBECONFIG` to that file.
- If the CLI reports `status: error` from the apply step, inspect the returned error string and `kubectl describe` the resource or `kubectl logs` for the controller. Common issues are RBAC or validation errors in the cluster.
- The project is a prototype: it shows the self-service workflow and applies resources, but production concerns (RBAC automation, hardened server-side apply, auditing) are listed in the README as future work.

Use this file as part of your project report or demo notes — copy-paste the command steps when you present the prototype.
