import json
import sys
sys.path.append('src')
from models.resident import Resident
from db import db

def test_add_resident(client):
    """Prueba para agregar un residente."""
    data = {"name": "Juan Pérez", "age": 70, "contact": "juan@example.com"}
    response = client.post('/residents', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    assert response.get_json()["id"] is not None
