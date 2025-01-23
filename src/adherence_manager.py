from flask import Blueprint, jsonify, request
import logging

app = Blueprint('adherence', __name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/adherence_activity.log"),
        logging.StreamHandler()
    ]
)

class AdherenceManager:
    def __init__(self):
        self.records = []

    def log_adherence(self, resident_id, medication_id, taken, timestamp):
        record = {
            "resident_id": resident_id,
            "medication_id": medication_id,
            "taken": taken,
            "timestamp": timestamp
        }
        self.records.append(record)
        return record

    def get_adherence(self, resident_id):
        return [record for record in self.records if record["resident_id"] == resident_id]

    def get_report(self):
        total = len(self.records)
        adherent = len([r for r in self.records if r["taken"]])
        adherence_rate = (adherent / total) * 100 if total > 0 else 0
        return {
            "total_records": total,
            "adherence_rate": adherence_rate
        }

adherence_manager = AdherenceManager()

@app.route('/adherence', methods=['POST'])
def log_adherence():
    data = request.get_json()
    resident_id = data.get("resident_id")
    medication_id = data.get("medication_id")
    taken = data.get("taken")
    timestamp = data.get("timestamp")

    if not all([resident_id, medication_id, taken is not None, timestamp]):
        return jsonify({"error": "Datos incompletos"}), 400

    record = adherence_manager.log_adherence(resident_id, medication_id, taken, timestamp)
    logging.info(f"Adherencia registrada: {record}")
    return jsonify({"message": "Adherencia registrada exitosamente.", "record": record}), 201

@app.route('/adherence/<int:resident_id>', methods=['GET'])
def get_adherence(resident_id):
    records = adherence_manager.get_adherence(resident_id)
    return jsonify({"resident_id": resident_id, "adherence": records}), 200

@app.route('/adherence/report', methods=['GET'])
def get_report():
    report = adherence_manager.get_report()
    return jsonify(report), 200
