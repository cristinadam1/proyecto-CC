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
