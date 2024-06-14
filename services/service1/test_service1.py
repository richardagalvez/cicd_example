from fastapi.testclient import TestClient

from service1 import app

client = TestClient(app)


def test_read_metadata():
    response = client.get("/metadata")
    assert response.status_code == 200
