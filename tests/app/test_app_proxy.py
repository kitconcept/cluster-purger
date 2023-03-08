from fastapi.testclient import TestClient
from cluster_purger.app import app
from pytest_httpx import HTTPXMock
import pytest

client = TestClient(app)


@pytest.fixture
def mock_all_purges(httpx_mock: HTTPXMock) -> HTTPXMock:
    httpx_mock.add_response(
        method="PURGE",
        match_headers={'user-agent': 'Swarm Purger'},
        status_code=200,
        headers={
            "x-cache": "12345"
        }
    )
    yield httpx_mock


def test_purge_remote_url_one_site(mock_all_purges, mock_with_1_site):
    response = client.request(method="PURGE", url="/de")
    assert response.status_code == 200
    requests = mock_all_purges.get_requests()
    assert len(requests) == 2
    request = requests[0]
    assert str(request.url) == "http://10.20.0.1/de"
    assert request.headers["host"] == "site.example.org"


def test_purge_remote_url_two_sites(mock_all_purges, mock_with_2_sites):
    response = client.request(method="PURGE", url="/de")
    assert response.status_code == 200
    requests = mock_all_purges.get_requests()
    assert len(requests) == 4
    request = requests[-1]
    assert str(request.url) == "http://10.20.0.2/de"
    assert request.headers["host"] == "cms.example.org"
