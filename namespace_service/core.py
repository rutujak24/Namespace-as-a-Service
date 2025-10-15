"""Core functions for namespace provisioning.

This is a minimal stub for Milestone 1. It provides a dry-run helper and
placeholders for create/delete namespace functions that will later call the
Kubernetes Python client.
"""

from typing import Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from . import monitor


TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"


def prepare_namespace_manifest(name: str, labels: Dict[str, str] | None = None) -> Dict:
    """Return a minimal namespace manifest dict.

    Args:
        name: namespace name
        labels: optional labels

    Returns:
        dict: Kubernetes Namespace manifest
    """
    return {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {
            "name": name,
            "labels": labels or {},
        },
    }


def create_namespace(
    name: str,
    dry_run: bool = True,
    cpu_request: str | None = None,
    cpu_limit: str | None = None,
    memory_request: str | None = None,
    memory_limit: str | None = None,
) -> Dict:
    """Create a namespace (stub).

    For Milestone 1 this will return the manifest and a message. Later we'll
    call the Kubernetes API.
    """
    # Render templates for resourcequota/limitrange alongside the namespace
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["yaml"]),
    )
    ns_manifest = prepare_namespace_manifest(name)
    rq_tmpl = env.get_template("resourcequota.yaml")
    lr_tmpl = env.get_template("limitrange.yaml")
    rq = rq_tmpl.render(
        name=name,
        cpu_request=cpu_request,
        cpu_limit=cpu_limit,
        memory_request=memory_request,
        memory_limit=memory_limit,
    )
    lr = lr_tmpl.render(
        name=name,
        default_memory=memory_limit,
        default_cpu=cpu_limit,
        request_memory=memory_request,
        request_cpu=cpu_request,
    )

    # Return combined artifacts for now
    if not dry_run:
        # increment created counter when actually applied
        monitor.inc_created()
    return {"status": "dry-run" if dry_run else "not-implemented", "namespace": ns_manifest, "resourcequota": rq, "limitrange": lr}


def delete_namespace(name: str, dry_run: bool = True) -> Dict:
    """Delete a namespace (stub)."""
    if dry_run:
        return {"status": "dry-run", "name": name}
    return {"status": "not-implemented", "name": name}
