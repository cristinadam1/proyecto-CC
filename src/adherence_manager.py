class AdherenceManager:
    def __init__(self):
        self.medication_logs = {}

    def log_medication(self, resident_id, timestamp, taken):
        if resident_id not in self.medication_logs:
            self.medication_logs[resident_id] = []
        self.medication_logs[resident_id].append({"timestamp": timestamp, "taken": taken})

    def calculate_adherence(self, resident_id):
        logs = self.medication_logs.get(resident_id, [])
        if not logs:
            return 0
        total = len(logs)
        taken = sum(1 for log in logs if log["taken"])
        return (taken / total) * 100

    def generate_alerts(self, resident_id):
        alerts = []
        logs = self.medication_logs.get(resident_id, [])
        for log in logs:
            if not log["taken"]:
                alerts.append({"resident_id": resident_id, "message": "El residente ha omitido su medicación."})
        return alerts
