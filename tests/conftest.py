import pytest
import sys
sys.path.append('src')
from app import app  
from db import db

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_db(client):
    """Fixture para limpiar la base de datos antes de cada prueba."""
    with client.application.app_context():
        db.session.remove()
        db.drop_all()  #Elimina todas las tablas de la base de datos
        db.create_all()  #Vuelve a crear las tablas vacías

