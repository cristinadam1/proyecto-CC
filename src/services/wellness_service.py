from datetime import datetime
import logging
from flask import Blueprint, jsonify, request
from models.wellness import WellnessTracking
from db import db

wellness_app = Blueprint('wellness', __name__)

#### POST ####
@wellness_app.route('/wellness', methods=['POST'])
def register_wellness():
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

#### GET ####
@wellness_app.route('/wellness', methods=['GET'])
def get_wellness_records():
    """Obtener todos los registros de bienestar."""
    registros = WellnessTracking.query.all()
    return jsonify([registro.to_dict() for registro in registros]), 200

#### DELETE ####
@wellness_app.route('/wellness/<int:resident_id>', methods=['DELETE'])
def remove_wellness(resident_id):
    wellness = WellnessTracking.query.get(resident_id)

    if not wellness:
        logging.error(f"Residente con ID {resident_id} no encontrado.")
        return jsonify({"error": "Residente no encontrado"}), 404

    db.session.delete(wellness)
    db.session.commit()
    logging.info(f"Wellnesses del residente con ID {resident_id} eliminado.")
    return jsonify({"message": "Wellnesses del residente eliminado"}), 200
