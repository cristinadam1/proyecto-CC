from db import db

# Modelo de Actividad
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)  # Duración en minutos
    ubicacion = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_hora": self.fecha_hora,
            "duracion": self.duracion,
            "ubicacion": self.ubicacion
        }


class ActivityParticipation(db.Model):
    __tablename__ = 'activity_participation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    residente_id = db.Column(db.Integer, nullable=False)  # Relación con residente
    estado = db.Column(db.String(50), nullable=False)  # "participó" o "ausente"
    observaciones = db.Column(db.String(255), nullable=True)
    

    def to_dict(self):
        return {
            "id": self.id,
            "activity_id": self.activity_id,
            "residente_id": self.residente_id,
            "estado": self.estado,
            "observaciones": self.observaciones
        }
