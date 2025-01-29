from db import db

class WellnessTracking(db.Model):
    __tablename__ = 'wellness_tracking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    residente_id = db.Column(db.Integer, nullable=False)  # Relación con residente
    fecha = db.Column(db.Date, nullable=False)
    estado_animo = db.Column(db.String(50), nullable=False)
    energia = db.Column(db.Integer, nullable=False)  # Del 1 al 10
    notas = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "residente_id": self.residente_id,
            "fecha": self.fecha,
            "estado_animo": self.estado_animo,
            "energia": self.energia,
            "notas": self.notas
        }