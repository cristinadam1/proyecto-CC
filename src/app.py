from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from resident_manager import resident_app, db

# Crear la app Flask
app = Flask(__name__)

# Configuración de la base de datos
db_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db')
if not os.path.exists(db_folder):
    os.makedirs(db_folder)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_folder, "microservices.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Para depurar las consultas SQL

# Inicializar la base de datos
db.init_app(app)

# Registrar el Blueprint de residentes
app.register_blueprint(resident_app)

# Crear las tablas en la base de datos
def create_db():
    with app.app_context():
        print("Creando las tablas en la base de datos...")
        db.create_all()
        print("Tablas creadas correctamente.")

# Ruta principal
@app.route('/')
def index():
    return "Servidor Flask funcionando correctamente con todos los microservicios."

# Crear la base de datos y ejecutar el servidor
if __name__ == '__main__':
    create_db()
    app.run(debug=True, port=5000)
