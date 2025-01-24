from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from resident_manager import resident_app
from medication_manager import medication_app
from prescription_manager import prescription_app
from db import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/prescriptions/*": {"origins": "*"}})


db_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db')
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Configuración de una única base de datos para todas las tablas
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_folder, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Para depurar las consultas SQL

db.init_app(app)

# Registrar los blueprints
app.register_blueprint(resident_app)
app.register_blueprint(medication_app)
app.register_blueprint(prescription_app)

# Crear las tablas en la base de datos
def create_db():
    with app.app_context():
        print("Creando las tablas en la base de datos...")
        db.create_all()  # Solo crea las tablas en la base de datos principal
        print("Tablas creadas correctamente.")

# Ruta principal
@app.route('/')
def index():
    return "Servidor Flask funcionando correctamente con todos los microservicios."

# Crear la base de datos y ejecutar el servidor
if __name__ == '__main__':
    create_db()
    app.run(debug=True, port=5000)
