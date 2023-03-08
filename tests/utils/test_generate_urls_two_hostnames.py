from urllib.parse import urlparse
import pytest


@pytest.fixture
def urls(mock_with_2_sites):
    from cluster_purger.utils import generate_urls

    return generate_urls(path="/de")


def test_generate_urls_with_two_hostnames_returns_4_urls(
    urls,
):
    assert len(urls) == 4


@pytest.mark.parametrize(
    "host",
    [
        "site.example.org",
        "cms.example.org",
    ]
)
def test_generate_urls_with_two_hostnames_returns_two_hostnames(
    urls,
    host: str
):
    hosts = {info.host for info in urls}
    assert len(hosts) == 2
    assert host in hosts


@pytest.mark.parametrize(
    "address",
    [
        "10.20.0.1",
        "10.20.0.2"
    ]
)
def test_generate_urls_with_two_hostnames_returns_two_addresses(
    urls,
    address: str
):
    addresses = {urlparse(info.url).hostname for info in urls}
    assert len(addresses) == 2
    assert address in addresses
