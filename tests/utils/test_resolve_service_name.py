import pytest

PORT = "SERVICE_PORT"


@pytest.fixture
def service_port_443(monkeypatch):
    from cluster_purger.config import settings

    if PORT in settings._deleted:
        settings._deleted.remove(PORT)
    with monkeypatch.context() as mp:
        mp.setenv(f"PURGER_{PORT}", "443")
        yield


@pytest.mark.parametrize(
    "service_name,scheme,expected",
    [
        ("varnish", "http", ["http://10.20.0.1", "http://10.20.0.2"],),
        ("varnish", "https", ["https://10.20.0.1", "https://10.20.0.2"],),
    ]
)
def test_resolve_service_name(service_name: str, scheme: str, expected: list[str]):
    from cluster_purger.utils import resolve_service_name

    result = resolve_service_name(service_name, scheme)
    assert len(result) == 2
    assert result[0] == expected[0]
    assert result[1] == expected[1]


def test_resolve_service_name_fail(mock_dns_resolve_fail):
    from cluster_purger.utils import resolve_service_name

    result = resolve_service_name("foo.bar")
    assert len(result) == 0


def test_resolve_service_name_with_port(service_port_443):
    from cluster_purger.utils import resolve_service_name

    result = resolve_service_name("varnish")
    assert len(result) == 2
    assert result[0] == "http://10.20.0.1:443"
