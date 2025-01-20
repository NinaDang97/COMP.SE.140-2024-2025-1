import pytest
import requests
from unittest.mock import patch
import subprocess

BASE_URL = 'http://localhost:8199' # URL for service1

@pytest.fixture(scope='module', autouse=True)
def start_service():
    """Ensure the service is started before testing."""
    yield
    # Stop the service after testing

def test_get_info():
    response = requests.get(BASE_URL)
    assert response.status_code == 200, "Expected status code 200 for GET /"
    data = response.json()
    assert "Service1" in data
    assert "Service2" in data