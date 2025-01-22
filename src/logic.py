
class Resident:
    def __init__(self, name, age, medication_schedule=None):
        if age < 0:
            raise ValueError("Age cannot be negative")
        self.name = name
        self.age = age
        self.medication_schedule = medication_schedule or []

    def add_medication(self, medication):
        if medication not in self.medication_schedule:
            self.medication_schedule.append(medication)


def generate_care_report(residents):
    return[
        {"name": resident.name, "age": resident.age, "medications": resident.medication_schedule}
        for resident in residents
    ]