"""Core functions for namespace provisioning.

This is a minimal stub for Milestone 1. It provides a dry-run helper and
placeholders for create/delete namespace functions that will later call the
Kubernetes Python client.
"""

from typing import Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


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


def create_namespace(name: str, dry_run: bool = True) -> Dict:
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
    rq = rq_tmpl.render(name=name)
    lr = lr_tmpl.render(name=name)

    # Return combined artifacts for now
    return {"status": "dry-run" if dry_run else "not-implemented", "namespace": ns_manifest, "resourcequota": rq, "limitrange": lr}


def delete_namespace(name: str, dry_run: bool = True) -> Dict:
    """Delete a namespace (stub)."""
    if dry_run:
        return {"status": "dry-run", "name": name}
    return {"status": "not-implemented", "name": name}
