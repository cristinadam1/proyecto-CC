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

def test_add_prescription_invalid_dates(client):
    """Prueba para agregar una prescripción con fechas inválidas"""
    data = {
        "resident_id": 1,
        "medication_id": 2,
        "dosage": "500mg",
        "frequency": "Cada 8 horas",
        "start_date": "2025-02-30",  # Fecha inválida (no existe el 30 de febrero)
        "end_date": "2025-02-31"      # Fecha inválida (no existe el 31 de febrero)
    }
    response = client.post('/prescriptions', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.get_json()["error"] == "Fecha de inicio inválida"  # Verifica que el error sea el esperado

def test_remove_prescription(client):
    """Prueba para eliminar una prescripción"""
    # Primero agregamos una prescripción
    data = {
        "resident_id": 1,
        "medication_id": 2,
        "dosage": "500mg",
        "frequency": "Cada 8 horas",
        "start_date": "2025-01-26",
        "end_date": "2025-02-02"
    }
    response = client.post('/prescriptions', data=json.dumps(data), content_type='application/json')
    prescription_id = response.get_json()["id"]

    # Ahora eliminamos la prescripción
    response = client.delete(f'/prescriptions/{prescription_id}')

    assert response.status_code == 200
    assert response.get_json()["message"] == "Prescripción eliminada"

    # Verificamos que la prescripción ya no exista
    response = client.get(f'/prescription/{prescription_id}')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Prescripción no encontrada"


def test_get_prescription_not_found(client):
    """Prueba para obtener una prescripción que no existe"""
    response = client.get('/prescription/9999')  # Asumimos que el ID 9999 no existe
    assert response.status_code == 404
    assert response.get_json()["error"] == "Prescripción no encontrada"


def test_get_all_prescriptions(client):
    """Prueba para obtener todas las prescripciones"""
    response = client.get('/prescriptions')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)  # Debe devolver una lista

def test_update_prescription_not_found(client):
    """Prueba para actualizar una prescripción que no existe"""
    data = {
        "dosage": "1000mg",
        "frequency": "Cada 12 horas"
    }
    response = client.put('/prescriptions/9999', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 404
    assert response.get_json()["error"] == "Prescripción no encontrada"

def test_update_prescription_invalid_data(client):
    """Prueba para actualizar una prescripción con datos inválidos (vacíos o nulos)"""
    # Primero agregamos una prescripción para tener algo que actualizar
    data = {
        "resident_id": 1,
        "medication_id": 2,
        "dosage": "500mg",
        "frequency": "Cada 8 horas",
        "start_date": "2025-01-26",
        "end_date": "2025-02-02"
    }
    response = client.post('/prescriptions', data=json.dumps(data), content_type='application/json')
    prescription_id = response.get_json()["id"]

    # Ahora intentamos actualizar la prescripción con un campo vacío
    invalid_data = {
        "dosage": "",  
        "frequency": None  
    }
    response = client.put(f'/prescriptions/{prescription_id}', data=json.dumps(invalid_data), content_type='application/json')

    # Verificamos que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.get_json()["error"] == "El campo 'dosage' no puede estar vacío"

# def test_update_prescription_valid_data(client):
#     """Prueba para actualizar una prescripción con datos válidos."""
#     # Crear una prescripción
#     data = {
#         "resident_id": 1,
#         "medication_id": 2,
#         "dosage": "500mg",
#         "frequency": "Cada 8 horas",
#         "start_date": "2025-01-26",
#         "end_date": "2025-02-02"
#     }
#     response = client.post('/prescriptions', data=json.dumps(data), content_type='application/json')
#     prescription_id = response.get_json()["id"]

#     # Actualizar la prescripción con nuevos datos
#     update_data = {
#         "dosage": "750mg",  # Actualizando la dosis
#         "frequency": "Cada 6 horas",  # Actualizando la frecuencia
#         "start_date": "2025-02-01",  # Actualizando la fecha de inicio
#         "end_date": "2025-02-15"  # Actualizando la fecha de fin
#     }
#     response = client.put(f'/prescriptions/{prescription_id}', data=json.dumps(update_data), content_type='application/json')

#     assert response.status_code == 200
#     assert response.get_json()["message"] == "Prescripción actualizada"

#     # Verificar que los datos se han actualizado
#     response = client.get(f'/prescription/{prescription_id}')
#     assert response.status_code == 200
#     prescription = response.get_json()
#     assert prescription["dosage"] == "750mg"
#     assert prescription["frequency"] == "Cada 6 horas"
#     assert prescription["start_date"] == "2025-02-01"
#     assert prescription["end_date"] == "2025-02-15"
