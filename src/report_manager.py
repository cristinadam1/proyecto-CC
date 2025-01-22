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
