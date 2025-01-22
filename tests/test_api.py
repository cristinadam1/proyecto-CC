import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_residents(client):
    response = client.get('/residents')
    assert response.status_code == 200
    assert "residents" in response.get_json()

def test_create_resident(client):
    response = client.post('/residents', json={"name": "John Doe"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Resident created successfully"

def test_get_resident_details(client):
    client.post('/residents', json={"name": "Jane Doe"})
    response = client.get('/residents/Jane Doe')
    assert response.status_code == 200
    assert response.get_json()["name"] == "Jane Doe"

def test_add_medication(client):
    client.post('/residents', json={"name": "John Doe"})
    response = client.post('/residents/John Doe', json={"medication": "Aspirin"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Medication added successfully"
