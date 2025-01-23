from flask import Flask, jsonify, request, Blueprint
import logging

#app = Flask(__name__)
app = Blueprint('report', __name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReportManager:
    def __init__(self, adherence_manager, resident_manager):
        self.adherence_manager = adherence_manager
        self.resident_manager = resident_manager

    def generate_resident_report(self, resident_id):
        resident = next((r for r in self.resident_manager.get_residents() if r["id"] == resident_id), None)
        if not resident:
            raise ValueError(f"Resident with ID {resident_id} does not exist.")
        adherence = self.adherence_manager.calculate_adherence(resident_id)
        return {"residente_id": resident_id, "adherencia": adherence}

    def generate_global_report(self):
        reports = []
        for resident in self.resident_manager.get_residents():
            resident_id = resident["id"]
            adherence = self.adherence_manager.calculate_adherence(resident_id)
            reports.append({"residente_id": resident_id, "adherencia": adherence})
        return reports

####### API ########
adherence_manager = None  # Sustituir con la instancia real de AdherenceManager
resident_manager = None   # Sustituir con la instancia real de ResidentManager
report_manager = ReportManager(adherence_manager, resident_manager)

# API de Flask
@app.route('/reports/resident/<int:resident_id>', methods=['GET'])
def get_resident_report(resident_id):
    """Ruta para obtener el reporte de un residente específico"""
    try:
        logging.info(f"Generando reporte para el residente con ID {resident_id}.")
        report = report_manager.generate_resident_report(resident_id)
        return jsonify(report), 200
    except ValueError as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 404

@app.route('/reports/global', methods=['GET'])
def get_global_report():
    """Ruta para obtener el reporte global de todos los residentes"""
    logging.info("Generando reporte global de todos los residentes.")
    reports = report_manager.generate_global_report()
    return jsonify(reports), 200

