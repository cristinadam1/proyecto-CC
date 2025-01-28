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

# import pytest
# import sys
# sys.path.append('src')
# from app import app as flask_app
# from db import db

# @pytest.fixture
# def app():
#     """Configura una instancia de la aplicación Flask para pruebas."""
#     flask_app.config['TESTING'] = True
#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#     flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     # Usamos la app que ya tiene db inicializado
#     with flask_app.app_context():
#         db.create_all()  # Crea las tablas en la base de datos en memoria
#         yield flask_app   # Retorna la app para que sea usada en los tests
#         db.drop_all()     # Limpia la base de datos después de cada test

# @pytest.fixture
# def client(app):
#     """Configura un cliente de pruebas para enviar solicitudes HTTP."""
#     return app.test_client()


