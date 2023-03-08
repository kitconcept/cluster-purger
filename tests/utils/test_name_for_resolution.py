import pytest

MODE = "MODE"

@pytest.fixture
def mode_compose(monkeypatch):
    from cluster_purger.config import settings

    if MODE in settings._deleted:
        settings._deleted.remove(MODE)
    with monkeypatch.context() as mp:
        mp.setenv("PURGER_MODE", "compose")
        yield


@pytest.fixture
def mode_swarm(monkeypatch):
    from cluster_purger.config import settings

    if MODE in settings._deleted:
        settings._deleted.remove(MODE)

    with monkeypatch.context() as mp:
        mp.setenv("PURGER_MODE", "swarm")
        yield


@pytest.fixture
def mode_other(monkeypatch):
    from cluster_purger.config import settings

    if MODE in settings._deleted:
        settings._deleted.remove(MODE)
    with monkeypatch.context() as mp:
        mp.setenv("PURGER_MODE", "kubernetes")
        yield


def test_name_for_resolution_compose(mode_compose):
    from cluster_purger.utils import name_for_resolution

    service_name = "varnish"
    result = name_for_resolution(service_name)
    assert result == "varnish"


def test_name_for_resolution_swarm(mode_swarm):
    from cluster_purger.utils import name_for_resolution

    service_name = "varnish"
    result = name_for_resolution(service_name)
    assert result == "tasks.varnish"


def test_name_for_resolution_other(mode_other):
    from cluster_purger.utils import name_for_resolution

    service_name = "varnish"
    result = name_for_resolution(service_name)
    assert result == "varnish"
