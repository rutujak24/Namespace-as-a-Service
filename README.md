# Namespace-as-a-Service (Simplified)

Minimal CLI to provision isolated Kubernetes namespaces with basic resource quotas and limit ranges.

Milestone 1: scaffold project and a CLI stub.

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
