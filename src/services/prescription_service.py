from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
from db import db
from models.prescription import Prescription
from datetime import datetime
#from sqlalchemy.orm import joinedload

prescription_app = Blueprint('prescriptions', __name__)

#### GET (todas) ####
@prescription_app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify([prescription.to_dict() for prescription in prescriptions]), 200

#### GET (por ID) ####
@prescription_app.route('/prescription/<int:prescription_id>', methods=['GET'])
def get_prescription(prescription_id):
    #prescription = Prescription.query.get(prescription_id)
    prescription = db.session.get(Prescription, prescription_id)
    #prescription = db.session.query(Prescription).options(joinedload(Prescription.resident)).get(prescription_id)

    if not prescription:
        logging.error(f"Prescription con ID {prescription_id} no encontrada.")
        return jsonify({"error": "Prescripción no encontrada"}), 404
    
    if not prescription.resident:
        logging.error(f"La prescripción con ID {prescription_id} no tiene un residente asociado.")
        return jsonify({"error": "Prescripción sin residente asociado"}), 404

    logging.info(f"Prescription con ID {prescription_id} obtenida.")
    return jsonify(prescription.to_dict()), 200

#### POST ####
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
    
    # Validación de datos de fecha
    if not is_valid_date(data.get("start_date")):
        logging.error("Fecha de inicio inválida.")
        return jsonify({"error": "Fecha de inicio inválida"}), 400

    if data.get("end_date") and not is_valid_date(data.get("end_date")):
        logging.error("Fecha de fin inválida.")
        return jsonify({"error": "Fecha de fin inválida"}), 400
    
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

#### PUT ####
@prescription_app.route('/prescriptions/<int:prescription_id>', methods=['PUT'])
def update_prescription(prescription_id):
    """Actualizar una prescripción"""
    data = request.get_json()
    #prescription = Prescription.query.get(prescription_id)
    prescription = db.session.get(Prescription, prescription_id)

    if not prescription:
        logging.error(f"Prescripción con ID {prescription_id} no encontrada.")
        return jsonify({"error": "Prescripción no encontrada"}), 404

    if "dosage" in data and not data["dosage"]:
        logging.error("El campo 'dosage' no puede estar vacío.")
        return jsonify({"error": "El campo 'dosage' no puede estar vacío"}), 400
    if "frequency" in data and not data["frequency"]:
        logging.error("El campo 'frequency' no puede estar vacío.")
        return jsonify({"error": "El campo 'frequency' no puede estar vacío"}), 400

    if "dosage" in data:
        prescription.dosage = data["dosage"]
    if "frequency" in data:
        prescription.frequency = data["frequency"]
    if "start_date" in data:
        prescription.start_date = data["start_date"]
    if "end_date" in data:
        prescription.end_date = data["end_date"]

    # db.session.commit()
    # logging.info(f"Prescripción con ID {prescription_id} actualizada.")
    # return jsonify({"message": "Prescripción actualizada"}), 200
        try:
            # Intentamos realizar el commit de la actualización
            db.session.commit()
            logging.info(f"Prescripción con ID {prescription_id} actualizada.")
            return jsonify({"message": "Prescripción actualizada"}), 200

        except Exception as e:
            # Si hay un error de base de datos, capturamos el error y devolvemos un 500
            db.session.rollback()
            logging.error(f"Error al actualizar la prescripción con ID {prescription_id}: {str(e)}")
            return jsonify({"error": "Error al actualizar la prescripción"}), 500

#### DELETE ####
@prescription_app.route('/prescriptions/<int:prescription_id>', methods=['DELETE'])
def remove_prescription(prescription_id):
    """Eliminar una prescripción"""
    #prescription = Prescription.query.get(prescription_id)
    prescription = db.session.get(Prescription, prescription_id)

    if not prescription:
        logging.error(f"Prescripción con ID {prescription_id} no encontrada.")
        return jsonify({"error": "Prescripción no encontrada"}), 404

    db.session.delete(prescription)
    db.session.commit()
    logging.info(f"Prescripción con ID {prescription_id} eliminada.")
    return jsonify({"message": "Prescripción eliminada"}), 200


def is_valid_date(date_string):
    """Función para validar si una fecha es válida (formato: YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")  # formato esperado: "2025-01-26"
        return True
    except ValueError:
        return False
