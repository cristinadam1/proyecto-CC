#Clase residente
class Resident:
    def __init__(self, name, age, medication_schedule=None):
        self.name = name
        self.age = age
        self.medication_schedule = medication_schedule or []

    def add_medication(self, medication):
        self.medication_schedule.append(medication)

#Generar reportes de cuidado
def generate_care_report(residents):
    return[
        {"name": resident.name, "age": resident.age, "medication": resident.medication_schedule}
        for resident in residents
    ]