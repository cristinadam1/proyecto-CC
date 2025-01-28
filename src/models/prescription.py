from db import db

class Prescription(db.Model):
    #__bind_key__ = 'prescriptions'
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id'), nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.id'), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=True)

    resident = db.relationship('Resident', backref=db.backref('prescriptions', lazy=True))
    medication = db.relationship('Medication', backref=db.backref('prescriptions', lazy=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "resident_id": self.resident_id,
            "medication_id": self.medication_id,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "resident_name": self.resident.name,
            "medication_name": self.medication.name
        }
    
    