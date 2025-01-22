class ResidentManager:
    def __init__(self):
        self.residents = {}
        self.next_id = 1

    def add_resident(self, name, age, contact):
        resident_id = self.next_id
        self.residents[resident_id] = {"name": name, "age": age, "contact": contact}
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
