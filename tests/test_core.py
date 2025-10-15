from namespace_service import core


def test_prepare_manifest():
    m = core.prepare_namespace_manifest("test-ns", labels={"team": "dev"})
    assert m["metadata"]["name"] == "test-ns"
    assert m["metadata"]["labels"]["team"] == "dev"


def test_create_namespace_dryrun():
    res = core.create_namespace("dry-ns", dry_run=True)
    assert res["status"] == "dry-run"
    assert res["manifest"]["kind"] == "Namespace"
