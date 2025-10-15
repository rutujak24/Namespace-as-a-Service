"""Kubernetes client wrapper.

Provides a minimal interface that can be mocked in tests. It lazily imports
the kubernetes client to avoid heavy test dependencies.
"""

from typing import Any, Dict
import tempfile
import os


class K8sClient:
    def __init__(self, kubeconfig: str | None = None):
        # Lazy import to avoid import-time dependency during tests
        from kubernetes import client, config, utils

        self._client = client
        self._config = config
        self._utils = utils
        self._kubeconfig = kubeconfig

        # Load configuration now (will raise if misconfigured when used)
        try:
            if kubeconfig:
                self._config.load_kube_config(config_file=kubeconfig)
            else:
                # try loading in-cluster, fall back to kubeconfig
                try:
                    self._config.load_incluster_config()
                except Exception:
                    self._config.load_kube_config()
        except Exception:
            # Let callers handle connectivity errors; tests will mock these imports
            pass

    def apply_manifest(self, manifest: Dict[str, Any] | str, dry_run: bool = True) -> Dict:
        """Apply a manifest to the cluster.

        Accepts either a Python dict (single resource) or a YAML string (possibly
        multi-document). Uses kubernetes.utils.create_from_yaml under the hood by
        writing a temporary file. Returns a dict with status and result or error.
        """
        if dry_run:
            return {"status": "dry-run", "manifest": manifest}

        try:
            # Ensure we have an ApiClient
            api_client = self._client.ApiClient()

            # Prepare YAML content
            if isinstance(manifest, dict):
                import yaml

                yaml_content = yaml.safe_dump(manifest)
            else:
                yaml_content = str(manifest)

            # Write to a temporary file and call create_from_yaml
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as tf:
                tf.write(yaml_content)
                tmpname = tf.name

            try:
                created = self._utils.create_from_yaml(api_client, tmpname)
            finally:
                try:
                    os.remove(tmpname)
                except Exception:
                    pass

            return {"status": "applied", "result": created}
        except Exception as e:
            return {"status": "error", "error": str(e)}


def default_client(kubeconfig: str | None = None) -> K8sClient:
    return K8sClient(kubeconfig=kubeconfig)
