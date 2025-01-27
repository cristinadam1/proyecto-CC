FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos del proyecto al contenedor
COPY . /app

# Instalación de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Puerto 5000 para la API
EXPOSE 5000

# Ejecutar la aplicación al iniciar el contenedor
CMD ["python", "src/app.py"]
