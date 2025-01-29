from db import db

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)  # Minutos
    ubicacion = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_hora": self.fecha_hora.isoformat() if self.fecha_hora else None,
            "duracion": self.duracion,
            "ubicacion": self.ubicacion
        }


