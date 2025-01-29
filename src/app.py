from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

sys.path.append('src')
from services.resident_service import resident_app
from services.wellness_service import wellness_app
from services.medication_service import medication_app
from services.prescription_service import prescription_app
from services.activity_service import activity_app
#from flasgger import Swagger
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from db import db
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#Swagger(app)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api_activity.log"),  
        logging.StreamHandler()                      
    ]
)

db_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db')
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Configuración de una única base de datos para todas las tablas
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_folder, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Para depurar las consultas SQL

db.init_app(app)

app.register_blueprint(resident_app)
app.register_blueprint(medication_app)
app.register_blueprint(prescription_app)
app.register_blueprint(activity_app)
app.register_blueprint(wellness_app)

# Swagger UI Configuration
SWAGGER_URL = "/seniorcare"
API_URL = "/static/swagger.yml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL,
    config={"app_name": "SeniorCare"}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Tablas en la base de datos
def create_db():
    with app.app_context():
        print("Creando las tablas en la base de datos...")
        db.create_all()  # Solo crea las tablas en la base de datos principal
        print("Tablas creadas correctamente.")

@app.route('/')
def index():
    return "Servidor Flask funcionando correctamente con todos los microservicios."

# Crear la base de datos y ejecutar el servidor
if __name__ == '__main__':
    create_db()
    #app.run(host='0.0.0.0', port=5000)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

