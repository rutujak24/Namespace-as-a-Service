import builtins
from unittest.mock import patch, MagicMock

from namespace_service.k8s import K8sClient


def test_apply_manifest_dict_dryrun():
    client = K8sClient()
    res = client.apply_manifest({"kind": "Namespace", "metadata": {"name": "x"}}, dry_run=True)
    assert res["status"] == "dry-run"


@patch("namespace_service.k8s.utils.create_from_yaml")
@patch("namespace_service.k8s.client.ApiClient")
def test_apply_manifest_dict_apply(mock_api, mock_create):
    mock_create.return_value = [MagicMock()]
    client = K8sClient()
    res = client.apply_manifest({"kind": "Namespace", "metadata": {"name": "x"}}, dry_run=False)
    assert res["status"] == "applied"


@patch("namespace_service.k8s.utils.create_from_yaml")
@patch("namespace_service.k8s.client.ApiClient")
def test_apply_manifest_yaml_apply(mock_api, mock_create):
    mock_create.return_value = [MagicMock()]
    client = K8sClient()
    yaml = "apiVersion: v1\nkind: Namespace\nmetadata:\n  name: y\n"
    res = client.apply_manifest(yaml, dry_run=False)
    assert res["status"] == "applied"
