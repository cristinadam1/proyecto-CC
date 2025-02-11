from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
from db import db
from models.medication import Medication

medication_app = Blueprint('medications', __name__)

#### GET (todas) ####
@medication_app.route('/medications', methods=['GET'])
def get_medications():
    medications = Medication.query.all()
    return jsonify([medication.to_dict() for medication in medications]), 200

#### POST ####
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

#### PUT ####
@medication_app.route('/medications/<int:medication_id>', methods=['PUT'])
def update_medication(medication_id):
    data = request.get_json()
    medication = db.session.get(Medication, medication_id)

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

#### DELETE ####
@medication_app.route('/medications/<int:medication_id>', methods=['DELETE'])
def remove_medication(medication_id):
    medication = db.session.get(Medication, medication_id)

    if not medication:
        logging.error(f"Medicación con ID {medication_id} no encontrada.")
        return jsonify({"error": "Medicación no encontrada"}), 404

    db.session.delete(medication)
    db.session.commit()
    logging.info(f"Medicación con ID {medication_id} eliminada.")
    return jsonify({"message": "Medicación eliminada"}), 200

#### GET (por ID) ####
@medication_app.route('/medications/<int:medication_id>', methods=['GET'])
def get_medication(medication_id):
    #medication = Medication.query.get(medication_id)
    medication = db.session.get(Medication, medication_id)

    if not medication:
        logging.error(f"Medicación con ID {medication_id} no encontrada.")
        return jsonify({"error": "Medicación no encontrada"}), 404

    logging.info(f"Medicación con ID {medication_id} obtenida.")
    return jsonify(medication.to_dict()), 200