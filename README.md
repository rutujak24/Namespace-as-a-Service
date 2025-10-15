# Namespace-as-a-Service

Minimal CLI to provision isolated Kubernetes namespaces with basic resource quotas and limit ranges.

This repository is a small Namespace-as-a-Service prototype implemented as an opinionated CLI. It renders parameterized Kubernetes manifests (Namespace, ResourceQuota, LimitRange) and provides a dry-run mode for safe testing.

Milestone 1–5: scaffold, template rendering, CLI, tests, CI, and a monitoring stub have been implemented. See "Project status" below for details.

Quickstart
---------

- Create a Python venv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Run the CLI (help):

```bash
./bin/nas --help
```

See `examples/create_namespace.sh` for a kubectl equivalent.

Project status — current milestone
---------------------------------

Implemented (prototype):
- CLI `bin/nas` (Click) with `create` and `delete` commands. Dry-run is the default mode.
- Parameterized Jinja2 templates in `templates/` for `ResourceQuota` and `LimitRange` and a sample `Namespace`.
- Template rendering pipeline in `namespace_service/core.py` that combines namespace + resource manifests.
- Lightweight `namespace_service/k8s.py` wrapper prepared for applying manifests (dry-run safe stub).
- Basic unit tests in `tests/` that validate manifest rendering and a monitoring stub.
- GitHub Actions CI workflow that runs tests.
- Monitoring stub with Prometheus metrics in `namespace_service/monitor.py`.

Limitations / Not implemented (production items):
- `k8s.K8sClient.apply_manifest()` is a placeholder. It does not perform server-side apply or handle API errors.
- No API server, web UI, authentication, or RBAC automation. The current flow is CLI-only.
- Templates are rendered to YAML strings; applying them should parse and validate YAML before sending to the API.
- More comprehensive tests (mocks for the real K8s client and e2e tests) are required.

Is this a Namespace-as-a-Service offering?
- Short answer: Yes, as a developer-facing prototype. It provides self-service provisioning via CLI, manifest generation, and a path to apply resources. To be a robust, multi-tenant Namespace-as-a-Service you'd still need to implement API, RBAC automation, hardened apply logic, and full testing.

Next steps to productionize (prioritized):
1. Implement Kubernetes apply/delete with server-side apply and YAML parsing.
2. Add authentication and an API layer (HTTP/gRPC) so teams can request namespaces programmatically.
3. Automate RBAC and tenant isolation (RoleBindings, quotas enforcement).
4. Expand tests: mock the Kubernetes client, add e2e with kind in CI, add linting and coverage reporting.
5. Improve observability and operational docs (metrics dashboards, runbook).

Contributing
------------
Contributions are welcome. Please open an issue or submit a pull request against the milestone branches. See the tests and CI for the current validation setup.

Demo and local testing
----------------------

This section shows how to run the project locally, run unit tests, and perform a small integration demo using `kind` (Kubernetes in Docker). The demo script below automates a simple workflow.

1) Ensure prerequisites

- Docker installed and running.
- `kind` and `kubectl` installed and on your PATH. See https://kind.sigs.k8s.io/ for install instructions.
- Python 3.9+ and system support for venv (`python3-venv` on Debian/Ubuntu).

2) Create a venv and install Python deps

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Run unit tests

```bash
pytest -q
```

4) Dry-run demo (no cluster)

```bash
./bin/nas create demo-ns --cpu-request 500m --memory-limit 1Gi
```

5) Full integration demo with `kind`

You can run the included demo script which will:
- create a temporary kind cluster
- run `./bin/nas create integration-ns --apply`
- show the namespace and associated resources
- delete the kind cluster when finished

Make the script executable and run it:

```bash
chmod +x scripts/demo_kind.sh
./scripts/demo_kind.sh
```

If you prefer to run the commands manually, the script performs these steps:

```bash
kind create cluster --name nas-demo
export KUBECONFIG="$(kind get kubeconfig-path --name=nas-demo)"
./bin/nas create integration-ns --apply
kubectl get ns
kubectl -n integration-ns get resourcequota,limitrange
kind delete cluster --name nas-demo
```

Notes
- The demo runs the project against a temporary kind cluster. The CLI uses the default kubeconfig; if you want to apply to a specific cluster, set `KUBECONFIG` before running.
- The `k8s` apply implementation uses `kubernetes.utils.create_from_yaml` and expects the Python Kubernetes client to be available in the venv.

