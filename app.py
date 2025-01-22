from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from src.logic import Resident

app = Flask(__name__)
api = Api(app)

@app.route("/z", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenido a la API de gestión de residentes"}), 200

# Simulación de una base de datos en memoria
residents = {}

class ResidentsAPI(Resource):
    def get(self):
        """Obtiene la lista de todos los residentes."""
        return jsonify({"residents": [res.to_dict() for res in residents.values()]})

    def post(self):
        """Crea un nuevo residente."""
        data = request.get_json()
        name = data.get("name")
        if not name:
            return {"error": "Name is required"}, 400
        if name in residents:
            return {"error": f"Resident {name} already exists."}, 400
        resident = Resident(name)
        residents[name] = resident
        return {"message": "Resident created successfully"}, 201

class ResidentDetailAPI(Resource):
    def get(self, name):
        """Obtiene los detalles de un residente específico."""
        resident = residents.get(name)
        if not resident:
            return {"error": "Resident not found"}, 404
        return jsonify(resident.to_dict())

    def post(self, name):
        """Añade un medicamento a un residente."""
        data = request.get_json()
        medication = data.get("medication")
        if not medication:
            return {"error": "Medication is required"}, 400
        resident = residents.get(name)
        if not resident:
            return {"error": "Resident not found"}, 404
        try:
            resident.add_medication(medication)
        except ValueError as e:
            return {"error": str(e)}, 400
        return {"message": "Medication added successfully"}, 200

# Definición de las rutas
api.add_resource(ResidentsAPI, '/residents')
api.add_resource(ResidentDetailAPI, '/residents/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)
