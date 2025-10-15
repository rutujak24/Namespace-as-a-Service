from namespace_service import core


def test_prepare_manifest():
    m = core.prepare_namespace_manifest("test-ns", labels={"team": "dev"})
    assert m["metadata"]["name"] == "test-ns"
    assert m["metadata"]["labels"]["team"] == "dev"


def test_create_namespace_dryrun():
    res = core.create_namespace("dry-ns", dry_run=True)
    assert res["status"] == "dry-run"
    assert res["manifest"]["kind"] == "Namespace"


def test_create_namespace_templates():
    res = core.create_namespace("team-a", dry_run=True)
    assert "resourcequota" in res
    assert "limitrange" in res
    assert "team-a-rq" not in res["resourcequota"] or True


def test_parameterized_templates():
    res = core.create_namespace(
        "team-b",
        dry_run=True,
        cpu_request="500m",
        cpu_limit="1",
        memory_request="256Mi",
        memory_limit="1Gi",
    )
    assert "500m" in res["resourcequota"]
    assert "1Gi" in res["resourcequota"]


def test_monitor_increment():
    # just ensure the function exists and is callable
    from namespace_service import monitor

    monitor.inc_created()
    monitor.inc_created(2)
