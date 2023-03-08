import pytest
import dns.resolver
from dataclasses import dataclass
from pytest import MonkeyPatch

SERVICE_NAME = "SERVICE_NAME"
SITES = "PUBLIC_SITES"


@dataclass
class MockRData:
    address: str


@pytest.fixture(autouse=True)
def mock_dns_resolve(monkeypatch: MonkeyPatch):
    """Mock a DNS response."""

    def mock_resolve(*args, **kwargs):

        return [
            MockRData("10.20.0.1"),
            MockRData("10.20.0.2"),
        ]

    monkeypatch.setattr(dns.resolver, "resolve", mock_resolve)


@pytest.fixture
def mock_dns_resolve_fail(monkeypatch: MonkeyPatch):
    """Raise error during resolve."""

    def mock_resolve(*args, **kwargs):

        raise dns.resolver.NoAnswer()

    monkeypatch.setattr(dns.resolver, "resolve", mock_resolve)

@pytest.fixture
def non_mocked_hosts() -> list:
    return ["testserver"]

@pytest.fixture(autouse=True)
def mock_service_name(monkeypatch):
    with monkeypatch.context() as mp:
        mp.setenv(f"PURGER_{SERVICE_NAME}", "varnish")
        yield

@pytest.fixture
def mock_with_1_site(monkeypatch: MonkeyPatch):
    from cluster_purger.config import settings

    if SITES in settings._deleted:
        settings._deleted.remove(SITES)
    with monkeypatch.context() as mp:
        mp.setenv(f"PURGER_{SITES}", "['site.example.org']")
        yield


@pytest.fixture
def mock_with_2_sites(monkeypatch: MonkeyPatch):
    from cluster_purger.config import settings

    if SITES in settings._deleted:
        settings._deleted.remove(SITES)
    with monkeypatch.context() as mp:
        mp.setenv(f"PURGER_{SITES}",
            "['site.example.org', 'cms.example.org']"
        )
        yield
