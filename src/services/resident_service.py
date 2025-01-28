import os
from flask import Blueprint, jsonify, request
import logging
from models.resident import Resident
from db import db

resident_app = Blueprint('residents', __name__)

#### GET (todos) ####
@resident_app.route('/residents', methods=['GET'])
def get_residents():
    residents = Resident.query.all()
    return jsonify([resident.to_dict() for resident in residents]), 200

#### GET (por ID) ####
@resident_app.route('/residents/<int:resident_id>', methods=['GET'])
def get_resident(resident_id):
    #resident = Resident.query.get(resident_id)
    resident = db.session.get(Resident, resident_id)

    if not resident:
        logging.error(f"Residente con ID {resident_id} no encontrado.")
        return jsonify({"error": "Residente no encontrado"}), 404

    logging.info(f"Residente con ID {resident_id} obtenida.")
    return jsonify(resident.to_dict()), 200

#### POST ####
@resident_app.route('/residents', methods=['POST'])
def add_resident():
    """Agregar un nuevo residente"""
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    contact = data.get("contact")

    if not name or not age or not contact:
        logging.error("Faltan datos en la petición.")
        return jsonify({"error": "Faltan datos"}), 400

    new_resident = Resident(name=name, age=age, contact=contact)
    db.session.add(new_resident)
    db.session.commit()

    logging.info(f"Residente {name} agregado con ID {new_resident.id}.")
    return jsonify({"id": new_resident.id}), 201

#### PUT ####
@resident_app.route('/residents/<int:resident_id>', methods=['PUT'])
def update_resident(resident_id):
    """Actualizar un residente"""
    data = request.get_json()
    #resident = Resident.query.get(resident_id)
    resident = db.session.get(Resident, resident_id)

    if not resident:
        logging.error(f"Residente con ID {resident_id} no encontrado.")
        return jsonify({"error": "Residente no encontrado"}), 404

    if "name" in data:
        resident.name = data["name"]
    if "age" in data:
        resident.age = data["age"]
    if "contact" in data:
        resident.contact = data["contact"]

    db.session.commit()
    logging.info(f"Residente con ID {resident_id} actualizado.")
    return jsonify({"message": "Residente actualizado"}), 200

#### DELETE ####
@resident_app.route('/residents/<int:resident_id>', methods=['DELETE'])
def remove_resident(resident_id):
    """Eliminar un residente"""
    #resident = Resident.query.get(resident_id)
    resident = db.session.get(Resident, resident_id)

    if not resident:
        logging.error(f"Residente con ID {resident_id} no encontrado.")
        return jsonify({"error": "Residente no encontrado"}), 404

    db.session.delete(resident)
    db.session.commit()

    logging.info(f"Residente con ID {resident_id} eliminado.")
    return jsonify({"message": "Residente eliminado"}), 200

    
    