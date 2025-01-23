from flask import Flask
import sys
sys.path.append('src')
from resident_manager import app as resident_app
from adherence_manager import app as adherence_app
from medication_manager import app as medication_app
from report_manager import app as report_app
import logging

# Aplicación principal
app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api_activity.log"),  # Guardar en un archivo
        logging.StreamHandler()                  # Mostrar en la consola
    ]
)

app.register_blueprint(resident_app)
app.register_blueprint(adherence_app)
app.register_blueprint(medication_app)
app.register_blueprint(report_app)

def index():
    return "Servidor Flask funcionando correctamente con todos los microservicios."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
