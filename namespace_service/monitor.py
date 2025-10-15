"""Simple monitoring helpers for Namespace-as-a-Service.

This is a tiny Prometheus metrics stub that exposes a counter for created
namespaces. It's intentionally minimal for the milestone.
"""

from prometheus_client import Counter

namespaces_created = Counter("nas_namespaces_created_total", "Total namespaces created")

def inc_created(count: int = 1):
    namespaces_created.inc(count)
