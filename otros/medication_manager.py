from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
from db import db

medication_app = Blueprint('medications', __name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[
    logging.FileHandler("logs/api_activity.log"),  
    logging.StreamHandler()
])

# Modelo Medication
class Medication(db.Model):
    #__bind_key__ = 'medications'
    __tablename__ = 'medications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    available_online = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "available_online": self.available_online
        }

# Rutas de la API para medicamentos (igual que antes)
@medication_app.route('/medications', methods=['GET'])
def get_medications():
    medications = Medication.query.all()
    return jsonify([medication.to_dict() for medication in medications]), 200


@medication_app.route('/medications', methods=['POST'])
def add_medication():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    available_online = data.get("available_online")

    if not name or not description or available_online is None:
        logging.error("Faltan datos en la petición.")
        return jsonify({"error": "Faltan datos"}), 400

    new_medication = Medication(name=name, description=description, available_online=available_online)
    db.session.add(new_medication)
    db.session.commit()

    logging.info(f"Medicación {name} agregada con ID {new_medication.id}.")
    return jsonify({"id": new_medication.id}), 201


@medication_app.route('/medications/<int:medication_id>', methods=['PUT'])
def update_medication(medication_id):
    data = request.get_json()
    medication = Medication.query.get(medication_id)

    if not medication:
        logging.error(f"Medicación con ID {medication_id} no encontrada.")
        return jsonify({"error": "Medicación no encontrada"}), 404

    if "name" in data:
        medication.name = data["name"]
    if "description" in data:
        medication.description = data["description"]
    if "available_online" in data:
        medication.available_online = data["available_online"]

    db.session.commit()
    logging.info(f"Medicación con ID {medication_id} actualizada.")
    return jsonify({"message": "Medicación actualizada"}), 200


@medication_app.route('/medications/<int:medication_id>', methods=['DELETE'])
def remove_medication(medication_id):
    medication = Medication.query.get(medication_id)

    if not medication:
        logging.error(f"Medicación con ID {medication_id} no encontrada.")
        return jsonify({"error": "Medicación no encontrada"}), 404

    db.session.delete(medication)
    db.session.commit()
    logging.info(f"Medicación con ID {medication_id} eliminada.")
    return jsonify({"message": "Medicación eliminada"}), 200
