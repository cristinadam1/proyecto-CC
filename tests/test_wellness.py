from datetime import datetime
import json
from models.wellness import WellnessTracking
from db import db

def test_register_wellness(client):
    """Prueba para registrar un nuevo seguimiento de bienestar."""
    data = {
        "residente_id": 1,
        "fecha": "2025-01-01",
        "estado_animo": "Feliz",
        "energia": 8,
        "notas": "Todo bien."
    }
    response = client.post('/wellness', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["residente_id"] == 1
    assert response_data["estado_animo"] == "Feliz"
    assert response_data["energia"] == 8
    assert response_data["notas"] == "Todo bien."

def test_register_wellness_missing_fields(client):
    """Prueba para registrar un seguimiento con campos faltantes."""
    data = {
        "residente_id": 1,
        "fecha": "2025-01-01"
        # Faltan "estado_animo" y "energia"
    }
    response = client.post('/wellness', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    response_data = response.get_json()
    assert "error" in response_data

def test_get_wellness_records(client):
    """Prueba para obtener todos los registros de bienestar."""
    with client.application.app_context():
        registro1 = WellnessTracking(
            residente_id=1,
            fecha=datetime(2025, 1, 1),
            estado_animo="Feliz",
            energia=8,
            notas="Todo bien."
        )
        registro2 = WellnessTracking(
            residente_id=2,
            fecha=datetime(2025, 1, 2),
            estado_animo="Triste",
            energia=5,
            notas="Se siente cansado."
        )
        db.session.add(registro1)
        db.session.add(registro2)
        db.session.commit()

    response = client.get('/wellness')
    assert response.status_code == 200
    response_data = response.get_json()
    assert len(response_data) == 2

    assert response_data[0]["residente_id"] == 1
    assert response_data[0]["estado_animo"] == "Feliz"
    assert response_data[1]["residente_id"] == 2
    assert response_data[1]["estado_animo"] == "Triste"
