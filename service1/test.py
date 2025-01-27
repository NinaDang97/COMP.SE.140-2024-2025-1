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
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "Service1" in data
    assert "Service2" in data

def test_get_state(client):
    response = client.get('/state')
    assert response.status_code == 200
    assert response.get_json() == "INIT"

def test_update_state(client):
    response = client.post('/state', data="RUNNING")
    assert response.status_code == 200
    assert response.get_json() == "RUNNING"

def test_invalid_state(client):
    response = client.post('/state', data="INVALID")
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid state"}

