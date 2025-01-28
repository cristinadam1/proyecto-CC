import json
import sys
sys.path.append('src')
from datetime import datetime
from models.activity import Activity
from db import db

def test_create_activity(client):
    """Prueba para crear una actividad."""
    data = {
        "nombre": "Yoga Matutino",
        "descripcion": "Sesión de yoga al aire libre",
        "fecha_hora": "2025-01-26T08:00:00",
        "duracion": 60,
        "ubicacion": "Patio central"
    }
    response = client.post('/activities', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["nombre"] == "Yoga Matutino"
    assert response_data["descripcion"] == "Sesión de yoga al aire libre"
    assert response_data["duracion"] == 60

def test_create_activity_missing_fields(client):
    """Prueba para crear actividad con campos obligatorios faltantes."""
    data = {"nombre": "Actividad sin fecha"}
    response = client.post('/activities', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.get_json()["error"] == "Faltan datos obligatorios"

def test_create_activity_invalid_date(client):
    """Prueba para crear actividad con fecha inválida."""
    data = {
        "nombre": "Yoga Matutino",
        "descripcion": "Sesión de yoga",
        "fecha_hora": "fecha-invalida",
        "duracion": 60,
        "ubicacion": "Patio central"
    }
    response = client.post('/activities', data=json.dumps(data), content_type='application/json')

    assert response.status_code == 400
    assert response.get_json()["error"] == "Formato de fecha inválido, usa ISO 8601"

def test_get_activities(client):
    # Limpiar las actividades existentes 
    with client.application.app_context():
        db.session.query(Activity).delete()  # Eliminar todas las actividades previas
        db.session.commit()  # Confirmar los cambios en la base de datos
    
        # Crear actividades para la prueba
        actividad1 = Activity(
            nombre="Yoga", descripcion="Relajación", 
            fecha_hora=datetime(2025, 1, 26, 8, 0), duracion=60, ubicacion="La zubia"
        )
        actividad2 = Activity(
            nombre="Meditación", descripcion="Meditación guiada", 
            fecha_hora=datetime(2025, 1, 26, 10, 0), duracion=30, ubicacion="Las Gabias"
        )
        db.session.add_all([actividad1, actividad2])
        db.session.commit()  # Asegurar que los datos se guarden en la base de datos

    response = client.get('/activities')

    assert response.status_code == 200
    response_data = response.get_json()

    assert len(response_data) == 2

def test_update_activity(client):
    """Prueba para actualizar una actividad existente."""
    # Primero, creamos una actividad
    data = {
        "nombre": "Yoga Matutino",
        "descripcion": "Sesión de yoga al aire libre",
        "fecha_hora": "2025-01-26T08:00:00",
        "duracion": 60,
        "ubicacion": "Patio central"
    }
    response = client.post('/activities', data=json.dumps(data), content_type='application/json')
    activity_id = response.get_json()["id"]

    # Ahora, intentamos actualizar la actividad
    updated_data = {
        "nombre": "Yoga Nocturno",
        "descripcion": "Sesión de yoga para relajación",
        "fecha_hora": "2025-01-26T20:00:00",
        "duracion": 90,
        "ubicacion": "Patio trasero"
    }
    response = client.put(f'/activities/{activity_id}', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["nombre"] == "Yoga Nocturno"
    assert response_data["descripcion"] == "Sesión de yoga para relajación"
    assert response_data["fecha_hora"] == "2025-01-26T20:00:00"

def test_update_activity_not_found(client):
    """Prueba para actualizar una actividad que no existe."""
    updated_data = {
        "nombre": "Yoga Nocturno",
        "descripcion": "Sesión de yoga para relajación",
        "fecha_hora": "2025-01-26T20:00:00",
        "duracion": 90,
        "ubicacion": "Patio trasero"
    }
    response = client.put('/activities/9999', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Actividad no encontrada"

def test_delete_activity(client):
    """Prueba para eliminar una actividad existente."""
    # Primero, creamos una actividad
    data = {
        "nombre": "Yoga Matutino",
        "descripcion": "Sesión de yoga al aire libre",
        "fecha_hora": "2025-01-26T08:00:00",
        "duracion": 60,
        "ubicacion": "Patio central"
    }
    response = client.post('/activities', data=json.dumps(data), content_type='application/json')
    activity_id = response.get_json()["id"]

    # Ahora, intentamos eliminar la actividad
    response = client.delete(f'/activities/{activity_id}')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Actividad eliminada exitosamente"

    # Verificamos que la actividad ya no existe
    response = client.get(f'/activities/{activity_id}')
    assert response.status_code == 404
    assert response.get_json()["error"] == "Actividad no encontrada"

def test_delete_activity_not_found(client):
    """Prueba para eliminar una actividad que no existe."""
    response = client.delete('/activities/9999')  
    assert response.status_code == 404
    assert response.get_json()["error"] == "Actividad no encontrada"

