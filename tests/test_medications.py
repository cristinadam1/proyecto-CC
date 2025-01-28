import json
import sys
sys.path.append('src')
from models.medication import Medication
from db import db

def test_add_medication(client):
    """Prueba para agregar un medicamento"""
    data = {"name": "Paracetamol", "description": "Alivia el dolor", "available_online": True}
    response = client.post('/medications', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    assert response.get_json()["id"] is not None

def test_add_medication_missing_fields(client):
    """Prueba para agregar medicamento con campos faltantes."""
    data = {"name": "Ibuprofeno"}
    response = client.post('/medications', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.get_json()["error"] == "Faltan datos"

def test_remove_medication(client):
    """Prueba para eliminar un medicamento."""
    with client.application.app_context():
        # Crear el medicamento en la base de datos
        medicamento = Medication(name="Amoxicilina", description="Antibiótico", available_online=False)
        db.session.add(medicamento)
        db.session.commit()

        medicamento = db.session.get(Medication, medicamento.id)
        response = client.delete(f'/medications/{medicamento.id}')
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Medicación eliminada"

        # Verificar que el medicamento ya no existe en la base de datos
        medicamento_eliminado = db.session.get(Medication, medicamento.id)
        assert medicamento_eliminado is None

def test_update_medication(client):
    """Prueba para actualizar un medicamento."""
    with client.application.app_context():
        # Crear el medicamento en la base de datos
        medicamento = Medication(name="Aspirina", description="Para el dolor", available_online=True)
        db.session.add(medicamento)
        db.session.commit()

        # Usar `Session.get()` para reconsultar el medicamento
        medicamento = db.session.get(Medication, medicamento.id)

        # Datos para la actualización
        data = {"description": "Analgésico actualizado"}

        # Hacer la solicitud PUT
        response = client.put(f'/medications/{medicamento.id}', data=json.dumps(data), content_type='application/json')

        # Verificar la respuesta
        assert response.status_code == 200
        assert response.get_json()["message"] == "Medicación actualizada"

        # Verificar que los datos se hayan actualizado correctamente
        medicamento_actualizado = db.session.get(Medication, medicamento.id)
        assert medicamento_actualizado.description == "Analgésico actualizado"

def test_get_all_medications(client):
    """Prueba para obtener todos los medicamentos."""
    with client.application.app_context():
        # Agregar medicamentos a la base de datos
        db.session.add(Medication(name="Paracetamol", description="Alivia el dolor", available_online=True))
        db.session.add(Medication(name="Ibuprofeno", description="Antiinflamatorio", available_online=False))
        db.session.commit()

        # Hacer la solicitud GET
        response = client.get('/medications')

        # Verificar la respuesta
        assert response.status_code == 200
        medications = response.get_json()
        assert len(medications) == 2
        assert medications[0]["name"] == "Paracetamol"
        assert medications[1]["name"] == "Ibuprofeno"

def test_get_all_medications_empty(client):
    """Prueba para obtener medicamentos cuando no hay ninguno."""
    response = client.get('/medications')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_medication_by_id(client):
    """Prueba para obtener un medicamento por su ID."""
    with client.application.app_context():
        # Crear un medicamento en la base de datos
        medicamento = Medication(name="Omeprazol", description="Protector gástrico", available_online=True)
        db.session.add(medicamento)
        db.session.commit()

        # Hacer la solicitud GET
        response = client.get(f'/medications/{medicamento.id}')
        assert response.status_code == 200
        assert response.get_json()["name"] == "Omeprazol"

def test_get_medication_not_found(client):
    """Prueba para obtener un medicamento con un ID que no existe."""
    response = client.get('/medications/9999')  # Un ID inexistente
    assert response.status_code == 404
    assert response.get_json()["error"] == "Medicación no encontrada"

def test_add_medication_invalid_data(client):
    """Prueba para agregar medicamento con datos inválidos."""
    # Falta un campo requerido
    data = {"description": "Solo descripción", "available_online": True}
    response = client.post('/medications', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert response.get_json()["error"] == "Faltan datos"

def test_update_nonexistent_medication(client):
    """Prueba para intentar actualizar un medicamento inexistente."""
    data = {"name": "Medicamento no existente"}
    response = client.put('/medications/9999', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Medicación no encontrada"

def test_remove_nonexistent_medication(client):
    """Prueba para eliminar un medicamento inexistente."""
    response = client.delete('/medications/9999')  # Un ID inexistente
    assert response.status_code == 404
    assert response.get_json()["error"] == "Medicación no encontrada"

