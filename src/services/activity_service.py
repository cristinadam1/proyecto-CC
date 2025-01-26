import logging
from flask import Blueprint, jsonify, request
from datetime import datetime
from db import db
from models.activity import Activity, ActivityParticipation

activity_app = Blueprint('activities', __name__)

#### POST ####
@activity_app.route('/activities', methods=['POST'])
def create_activity():
    """Crear una nueva actividad"""
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    fecha_hora = data.get('fecha_hora')
    duracion = data.get('duracion')
    ubicacion = data.get('ubicacion')

    if not nombre or not fecha_hora or not duracion:
        logging.error("Faltan datos obligatorios para crear la actividad.")
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    try:
        fecha_hora = datetime.fromisoformat(fecha_hora)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido, usa ISO 8601"}), 400

    nueva_actividad = Activity(
        nombre=nombre, descripcion=descripcion, fecha_hora=fecha_hora,
        duracion=duracion, ubicacion=ubicacion
    )
    db.session.add(nueva_actividad)
    db.session.commit()

    logging.info(f"Actividad {nombre} creada con ID {nueva_actividad.id}.")
    return jsonify(nueva_actividad.to_dict()), 201

#### GET (todas) ####
@activity_app.route('/activities', methods=['GET'])
def get_activities():
    actividades = Activity.query.all()
    return jsonify([actividad.to_dict() for actividad in actividades]), 200

#### GET (por ID) ####
@activity_app.route('/activities/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    actividad = Activity.query.get(activity_id)
    if not actividad:
        logging.error(f"Actividad con ID {activity_id} no encontrada.")
        return jsonify({"error": "Actividad no encontrada"}), 404

    return jsonify(actividad.to_dict()), 200

#### PUT ####
@activity_app.route('/activities/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    actividad = Activity.query.get(activity_id)
    if not actividad:
        logging.error(f"Actividad con ID {activity_id} no encontrada para actualización.")
        return jsonify({"error": "Actividad no encontrada"}), 404

    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    fecha_hora = data.get('fecha_hora')
    duracion = data.get('duracion')
    ubicacion = data.get('ubicacion')

    try:
        if fecha_hora:
            fecha_hora = datetime.fromisoformat(fecha_hora)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido, usa ISO 8601"}), 400

    if nombre:
        actividad.nombre = nombre
    if descripcion:
        actividad.descripcion = descripcion
    if fecha_hora:
        actividad.fecha_hora = fecha_hora
    if duracion:
        actividad.duracion = duracion
    if ubicacion:
        actividad.ubicacion = ubicacion

    db.session.commit()
    logging.info(f"Actividad con ID {activity_id} actualizada.")
    return jsonify(actividad.to_dict()), 200

#### DELETE ####
@activity_app.route('/activities/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    actividad = Activity.query.get(activity_id)
    if not actividad:
        logging.error(f"Actividad con ID {activity_id} no encontrada para eliminación.")
        return jsonify({"error": "Actividad no encontrada"}), 404

    db.session.delete(actividad)
    db.session.commit()
    logging.info(f"Actividad con ID {activity_id} eliminada.")
    return jsonify({"message": "Actividad eliminada exitosamente"}), 200

# @activity_app.route('/activities/<int:activity_id>/participation', methods=['POST'])
# def add_participation(activity_id):
#     """Registrar la participación de un residente en una actividad."""
#     data = request.get_json()
#     residente_id = data.get('residente_id')
#     estado = data.get('estado')
#     observaciones = data.get('observaciones')

#     if not residente_id or not estado:
#         logging.error("Faltan datos obligatorios para registrar la participación.")
#         return jsonify({"error": "Faltan datos obligatorios"}), 400

#     nueva_participacion = ActivityParticipation(
#         activity_id=activity_id, residente_id=residente_id,
#         estado=estado, observaciones=observaciones
#     )
#     db.session.add(nueva_participacion)
#     db.session.commit()

#     logging.info(f"Participación registrada para actividad {activity_id}, residente {residente_id}.")
#     return jsonify(nueva_participacion.to_dict()), 201
