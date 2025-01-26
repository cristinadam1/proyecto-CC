from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
from db import db
from models.prescription import Prescription

# Crear el Blueprint
prescription_app = Blueprint('prescriptions', __name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[
    logging.FileHandler("logs/api_activity.log"),  
    logging.StreamHandler()
])

# Rutas de la API para prescripciones
@prescription_app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    """Obtener todas las prescripciones"""
    prescriptions = Prescription.query.all()
    return jsonify([prescription.to_dict() for prescription in prescriptions]), 200

@prescription_app.route('/prescriptions', methods=['POST'])
def add_prescription():
    """Agregar una nueva prescripción"""
    data = request.get_json()
    resident_id = data.get("resident_id")
    medication_id = data.get("medication_id")
    dosage = data.get("dosage")
    frequency = data.get("frequency")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not resident_id or not medication_id or not dosage or not frequency or not start_date:
        logging.error("Faltan datos en la petición.")
        return jsonify({"error": "Faltan datos"}), 400

    new_prescription = Prescription(
        resident_id=resident_id, 
        medication_id=medication_id, 
        dosage=dosage, 
        frequency=frequency, 
        start_date=start_date, 
        end_date=end_date
    )
    db.session.add(new_prescription)
    db.session.commit()

    logging.info(f"Prescripción agregada con ID {new_prescription.id}.")
    return jsonify({"id": new_prescription.id}), 201

@prescription_app.route('/prescriptions/<int:prescription_id>', methods=['PUT'])
def update_prescription(prescription_id):
    """Actualizar una prescripción"""
    data = request.get_json()
    prescription = Prescription.query.get(prescription_id)

    if not prescription:
        logging.error(f"Prescripción con ID {prescription_id} no encontrada.")
        return jsonify({"error": "Prescripción no encontrada"}), 404

    if "dosage" in data:
        prescription.dosage = data["dosage"]
    if "frequency" in data:
        prescription.frequency = data["frequency"]
    if "start_date" in data:
        prescription.start_date = data["start_date"]
    if "end_date" in data:
        prescription.end_date = data["end_date"]

    db.session.commit()
    logging.info(f"Prescripción con ID {prescription_id} actualizada.")
    return jsonify({"message": "Prescripción actualizada"}), 200

@prescription_app.route('/prescriptions/<int:prescription_id>', methods=['DELETE'])
def remove_prescription(prescription_id):
    """Eliminar una prescripción"""
    prescription = Prescription.query.get(prescription_id)

    if not prescription:
        logging.error(f"Prescripción con ID {prescription_id} no encontrada.")
        return jsonify({"error": "Prescripción no encontrada"}), 404

    db.session.delete(prescription)
    db.session.commit()
    logging.info(f"Prescripción con ID {prescription_id} eliminada.")
    return jsonify({"message": "Prescripción eliminada"}), 200

#