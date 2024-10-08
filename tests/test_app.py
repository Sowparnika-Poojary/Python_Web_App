# tests/test_app.py

import pytest
from app import app  # Import your Flask app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    with app.test_client() as client:
        yield client  # This will be your test client for making requests

def test_homepage(client):
    """Test the homepage of the Flask application."""
    response = client.get('/')  # Simulate a GET request to the homepage
    assert response.status_code == 200  # Check if the response status is 200 OK
    assert b"Welcome to IQVIA!" in response.data  # Check the response content
