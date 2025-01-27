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

