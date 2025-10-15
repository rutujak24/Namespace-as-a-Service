"""Core functions for namespace provisioning.

This is a minimal stub for Milestone 1. It provides a dry-run helper and
placeholders for create/delete namespace functions that will later call the
Kubernetes Python client.
"""

from typing import Dict


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
    manifest = prepare_namespace_manifest(name)
    if dry_run:
        return {"status": "dry-run", "manifest": manifest}
    # TODO: implement actual kubernetes client call
    return {"status": "not-implemented", "manifest": manifest}


def delete_namespace(name: str, dry_run: bool = True) -> Dict:
    """Delete a namespace (stub)."""
    if dry_run:
        return {"status": "dry-run", "name": name}
    return {"status": "not-implemented", "name": name}
