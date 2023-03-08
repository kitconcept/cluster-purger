from fastapi.testclient import TestClient
from cluster_purger.app import app
from typing import Any
import pytest

client = TestClient(app)

@pytest.fixture
def get_info_1(mock_with_1_site):
    return client.get("/info")


@pytest.fixture
def get_info_2(mock_with_2_sites):
    return client.get("/info")


@pytest.mark.parametrize(
    "key,expected",
    [
        ["service_name", "varnish"],
        ["addresses", ["http://10.20.0.1", "http://10.20.0.2"]],
        ["hostnames", ["site.example.org" ]],
    ]
)
def test_info_one_hostname(get_info_1, key: str, expected: Any):
    response = get_info_1.json()
    assert response[key] == expected


@pytest.mark.parametrize(
    "key,expected",
    [
        ["service_name", "varnish"],
        ["addresses", ["http://10.20.0.1", "http://10.20.0.2"]],
        ["hostnames", ["site.example.org", "cms.example.org"]],
    ]
)
def test_info_two_hostnames(get_info_2, key: str, expected: Any):
    response = get_info_2.json()
    assert response[key] == expected
