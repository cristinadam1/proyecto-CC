import json
import sys
sys.path.append('src')
from models.prescription import Prescription
from db import db

def test_add_prescription(client):
    """Prueba para agregar una prescripción"""
    data = {
        "resident_id": 1,
        "medication_id": 2,
        "dosage": "500mg",
        "frequency": "Cada 8 horas",
        "start_date": "2025-01-26",
        "end_date": "2025-02-02"
    }
    response = client.post('/prescriptions', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    assert response.get_json()["id"] is not None

def test_add_prescription_missing_fields(client):
    """Prueba para agregar prescripción con campos faltantes"""
    data = {"resident_id": 1}
    response = client.post('/prescriptions', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.get_json()["error"] == "Faltan datos"
