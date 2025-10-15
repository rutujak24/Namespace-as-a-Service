"""Kubernetes client wrapper.

Provides a minimal interface that can be mocked in tests. It lazily imports
the kubernetes client to avoid heavy test dependencies.
"""

from typing import Any, Dict


class K8sClient:
    def __init__(self, kubeconfig: str | None = None):
        # Lazy import to avoid import-time dependency during tests
        try:
            from kubernetes import client, config
        except Exception:  # pragma: no cover - real runtime only
            client = None
            config = None

        self._client = client
        self._config = config

    def apply_manifest(self, manifest: Dict[str, Any], dry_run: bool = True) -> Dict:
        """Apply a manifest to the cluster (very small wrapper).

        For Milestone 2 this method supports dry_run only. Real implementations
        will use server-side apply or create calls.
        """
        if dry_run:
            return {"status": "dry-run", "manifest": manifest}
        # TODO: implement using kubernetes.client API
        return {"status": "not-implemented"}


def default_client(kubeconfig: str | None = None) -> K8sClient:
    return K8sClient(kubeconfig=kubeconfig)
