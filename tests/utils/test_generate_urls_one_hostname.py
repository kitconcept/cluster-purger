from urllib.parse import urlparse
import pytest


@pytest.fixture
def urls(mock_with_1_site):
    from cluster_purger.utils import generate_urls

    return generate_urls(path="/de")


def test_generate_urls_with_one_hostname_returns_2_urls(
    urls,
):
    assert len(urls) == 2


@pytest.mark.parametrize(
    "host",
    [
        "site.example.org"
    ]
)
def test_generate_urls_with_one_hostname_returns_one_hostname(
    urls,
    host: str
):
    hosts = {info.host for info in urls}
    assert len(hosts) == 1
    assert host in hosts


@pytest.mark.parametrize(
    "address",
    [
        "10.20.0.1",
        "10.20.0.2"
    ]
)
def test_generate_urls_with_one_hostname_returns_two_addresses(
    urls,
    address: str
):
    addresses = {urlparse(info.url).hostname for info in urls}
    assert len(addresses) == 2
    assert address in addresses



def test_generate_urls_returns_2_urls(urls):
    from cluster_purger.utils import generate_urls

    urls = generate_urls(path="/de")
    assert len(urls) == 2


def test_generate_urls_returns_one_hostname():
    from cluster_purger.utils import generate_urls

    urls = generate_urls(path="/de")
    hosts = list({info.host for info in urls})
    assert len(hosts) == 1
    assert hosts[0] == ""


@pytest.mark.parametrize(
    "address",
    [
        "10.20.0.1",
        "10.20.0.2"
    ]
)
def test_generate_urls_returns_two_addresses(address: str):
    from cluster_purger.utils import generate_urls

    urls = generate_urls(path="/de")
    addresses = {urlparse(info.url).hostname for info in urls}
    assert len(addresses) == 2
    assert address in addresses


def test_generate_urls_with_fail_in_service_resolution(mock_dns_resolve_fail):
    from cluster_purger.utils import generate_urls

    urls = generate_urls(path="/de")
    assert len(urls) == 0
