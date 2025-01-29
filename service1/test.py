import pytest
from service import app

BASE_URL = 'http://localhost:8197' # URL for service1

# Mock test
def test():
    assert 1 == 1

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_info_data(client):
    response = client.get('/request')
    assert response.status_code == 200
    data = response.get_json()
    assert "Service1" in data
    assert "Service2" in data

def test_get_state(client):
    response = client.get('/state')
    assert response.status_code == 200
    assert response.get_json() == "INIT"

def test_update_state(client):
    response = client.get('/state')
    assert response.status_code == 200
    assert response.get_json() == "INIT"
    response1 = client.put('/state', data="RUNNING")
    assert response1.status_code == 200
    assert response1.get_json() == "RUNNING"
    response2 = client.get('/state')
    assert response2.status_code == 200
    assert response2.get_json() == "RUNNING"


def test_invalid_state(client):
    response = client.put('/state', data="INVALID")
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid state"}

def test_run_log(client):
    client.put("/state", data="RUNNING", content_type="text/plain")
    client.put("/state", data="PAUSED", content_type="text/plain")

    response = client.get('/run-log')

    assert response.status_code == 200
    assert response.content_type == "text/plain"
    log_lines = response.data.decode("utf-8").split("\n")
    assert "INIT->RUNNING" in log_lines[0]
    assert "RUNNING->PAUSED" in log_lines[1]