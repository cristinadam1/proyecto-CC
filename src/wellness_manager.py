from datetime import datetime
import logging
from flask import Blueprint, jsonify, request
from db import db

wellness_app = Blueprint('wellness', __name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[
    logging.FileHandler("logs/wellness_tracking.log"),
    logging.StreamHandler()
])

# Modelo de Seguimiento del Bienestar
class WellnessTracking(db.Model):
    __tablename__ = 'wellness_tracking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    residente_id = db.Column(db.Integer, nullable=False)  # Relación con residente
    fecha = db.Column(db.Date, nullable=False)
    estado_animo = db.Column(db.String(50), nullable=False)
    energia = db.Column(db.Integer, nullable=False)  # Escala del 1 al 10
    notas = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "residente_id": self.residente_id,
            "fecha": self.fecha,
            "estado_animo": self.estado_animo,
            "energia": self.energia,
            "notas": self.notas
        }

# Rutas del módulo
@wellness_app.route('/wellness', methods=['POST'])
def register_wellness():
    """Registrar el bienestar de un residente."""
    data = request.get_json()
    residente_id = data.get('residente_id')
    fecha = data.get('fecha')
    estado_animo = data.get('estado_animo')
    energia = data.get('energia')
    notas = data.get('notas')

    if not residente_id or not fecha or not estado_animo or energia is None:
        logging.error("Faltan datos obligatorios para registrar el bienestar.")
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Convertir fecha_hora en un objeto datetime
        fecha = datetime.fromisoformat(fecha)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido, usa ISO 8601"}), 400

    nuevo_registro = WellnessTracking(
        residente_id=residente_id, fecha=fecha,
        estado_animo=estado_animo, energia=energia, notas=notas
    )
    db.session.add(nuevo_registro)
    db.session.commit()

    logging.info(f"Bienestar registrado para residente {residente_id} en la fecha {fecha}.")
    return jsonify(nuevo_registro.to_dict()), 201


@wellness_app.route('/wellness', methods=['GET'])
def get_wellness_records():
    """Obtener todos los registros de bienestar."""
    registros = WellnessTracking.query.all()
    return jsonify([registro.to_dict() for registro in registros]), 200
