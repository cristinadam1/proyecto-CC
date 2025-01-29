import json
import sys
sys.path.append('src')
from models.resident import Resident
from db import db

def test_add_resident(client):
    data = {"name": "Juan Pérez", "age": 70, "contact": "juan@example.com"}
    response = client.post('/residents', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    assert response.get_json()["id"] is not None

def test_get_residents(client):
    # Verifica que si no hay residentes, la respuesta sea vacía
    response = client.get('/residents')
    assert response.status_code == 200
    assert response.json == []

    # Agregar un residente para la siguiente prueba
    resident = Resident(name="Juan", age=80, contact="609432167")
    db.session.add(resident)
    db.session.commit()

    # Verifica que la respuesta contenga el residente agregado
    response = client.get('/residents')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == "Juan"


def test_add_resident_missing_data(client):
    data = {"name": "Laura", "age": 50}  # Falta el campo "contact"
    response = client.post('/residents', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.json["error"] == "Faltan datos"

def test_delete_resident(client):
    # Crear un residente primero
    data = {"name": "Juan Pérez", "age": 70, "contact": "juan@example.com"}
    response = client.post('/residents', data=json.dumps(data), content_type='application/json')
    resident_id = response.get_json()["id"]
    
    # Eliminar el residente
    response = client.delete(f'/residents/{resident_id}')
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Residente eliminado"
    
    # Verificar que el residente ya no existe
    response = client.get(f'/residents/{resident_id}')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Residente no encontrado"

def test_update_resident(client):
    # Crear un residente
    data = {"name": "Juan Pérez", "age": 70, "contact": "juan@example.com"}
    response = client.post('/residents', data=json.dumps(data), content_type='application/json')
    resident_id = response.get_json()["id"]
    
    # Actualizar el residente
    update_data = {"name": "Juan Pérez Actualizado", "age": 71}
    response = client.put(f'/residents/{resident_id}', data=json.dumps(update_data), content_type='application/json')
    
    assert response.status_code == 200
    assert response.get_json()["message"] == "Residente actualizado"
    
    # Verificar que los datos se actualicen
    response = client.get(f'/residents/{resident_id}')
    assert response.get_json()["name"] == "Juan Pérez Actualizado"
    assert response.get_json()["age"] == 71
