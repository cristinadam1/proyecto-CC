# src/medication_manager.py
from flask import Flask, jsonify, request, Blueprint
import logging

# Configuración básica de Flask
#app = Flask(__name__)
app = Blueprint('medication', __name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MedicationManager:
    def __init__(self):
        self.medications = {}
        self.next_id = 1

    def add_medication(self, name, description, available_online):
        medication_id = self.next_id
        self.medications[medication_id] = {
            "name": name,
            "description": description,
            "available_online": available_online,
        }
        self.next_id += 1
        return medication_id

    def update_medication(self, medication_id, **updates):
        if medication_id in self.medications:
            self.medications[medication_id].update(updates)
        else:
            raise ValueError(f"Medication with ID {medication_id} does not exist.")

    def remove_medication(self, medication_id):
        if medication_id in self.medications:
            del self.medications[medication_id]
        else:
            raise ValueError(f"Medication with ID {medication_id} does not exist.")

    def get_medications(self):
        return list(self.medications.values())


####### API ########
medication_manager = MedicationManager()

# API de Flask
@app.route('/medication', methods=['GET'])
def get_medications():
    """Ruta para obtener todas las medicinas registradas"""
    medications = medication_manager.get_medications()
    return jsonify(medications), 200

@app.route('/medication', methods=['POST'])
def add_medication():
    """Ruta para añadir una nueva medicina"""
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    available_online = data.get("available_online")

    if not name or not description or available_online is None:
        return jsonify({"error": "Datos inválidos"}), 400

    medication_id = medication_manager.add_medication(name, description, available_online)
    logging.info(f"Medicina añadida: {name}, ID: {medication_id}.")
    return jsonify({"message": "Medicina añadida exitosamente.", "medication_id": medication_id}), 201

@app.route('/medication/<int:medication_id>', methods=['PUT'])
def update_medication(medication_id):
    """Ruta para actualizar los detalles de una medicina"""
    data = request.get_json()
    updates = {key: value for key, value in data.items() if value is not None}
    
    try:
        medication_manager.update_medication(medication_id, **updates)
        return jsonify({"message": "Medicina actualizada exitosamente."}), 200
    except ValueError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 404

@app.route('/medication/<int:medication_id>', methods=['DELETE'])
def remove_medication(medication_id):
    """Ruta para eliminar una medicina"""
    try:
        medication_manager.remove_medication(medication_id)
        return jsonify({"message": "Medicina eliminada exitosamente."}), 200
    except ValueError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 404