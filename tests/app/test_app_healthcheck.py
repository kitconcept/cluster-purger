from fastapi.testclient import TestClient
from cluster_purger.app import app


client = TestClient(app)


def test_healthcheck():
    response = client.get("/ok")
    assert response.status_code == 200
    assert response.json() == "Ok"
