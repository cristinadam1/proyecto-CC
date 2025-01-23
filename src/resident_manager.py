from flask import Flask, jsonify, request
import logging
# Configuración básica de Flask
app = Flask(__name__)

# Configuración de logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración avanzada de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api_activity.log"),  # Guardar en un archivo
        logging.StreamHandler()                  # Mostrar en la consola
    ]
)

class ResidentManager:
    def __init__(self):
        self.residents = {}
        self.next_id = 1

    def add_resident(self, name, age, contact):
        resident_id = self.next_id
        self.residents[resident_id] = {"id": resident_id,"name": name, "age": age, "contact": contact}
        self.next_id += 1
        return resident_id

    def update_resident(self, resident_id, **updates):
        if resident_id in self.residents:
            self.residents[resident_id].update(updates)
        else:
            raise ValueError(f"Resident with ID {resident_id} does not exist.")

    def remove_resident(self, resident_id):
        if resident_id in self.residents:
            del self.residents[resident_id]
        else:
            raise ValueError(f"Resident with ID {resident_id} does not exist.")

    def get_residents(self):
        return list(self.residents.values())

# Instancia de ResidentManager
resident_manager = ResidentManager()

# API de Flask
@app.route('/residents', methods=['GET'])
def get_residents():
    """Ruta para obtener todos los residentes"""
    logging.info("Obteniendo todos los residentes.")
    residents = resident_manager.get_residents()
    return jsonify(residents), 200

@app.route('/residents', methods=['POST'])
def add_resident():
    """Ruta para agregar un residente"""
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    contact = data.get("contact")

    if not name or not age or not contact:
        logging.error("Faltan datos en la petición.")
        return jsonify({"error": "Faltan datos"}), 400

    resident_id = resident_manager.add_resident(name, age, contact)
    logging.info(f"Residente {name} agregado con ID {resident_id}.")
    return jsonify({"id": resident_id}), 201

@app.route('/residents/<int:resident_id>', methods=['PUT'])
def update_resident(resident_id):
    """Ruta para modificar un residente"""
    data = request.get_json()
    try:
        resident_manager.update_resident(resident_id, **data)
        logging.info(f"Residente con ID {resident_id} actualizado.")
        return jsonify({"message": "Residente actualizado."}), 200
    except ValueError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 404

@app.route('/residents/<int:resident_id>', methods=['DELETE'])
def remove_resident(resident_id):
    """Ruta para eliminar un residente"""
    try:
        resident_manager.remove_resident(resident_id)
        logging.info(f"Residente con ID {resident_id} eliminado.")
        return jsonify({"message": "Residente eliminado."}), 200
    except ValueError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)