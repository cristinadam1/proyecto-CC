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
