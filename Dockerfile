FROM python:3.10-slim

WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt requirements.txt

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/logs


# Copiar el código de la aplicación
COPY src/ /app/src/

# Exponer el puerto de la API
EXPOSE 5000

# Comando para ejecutar la aplicación
#CMD ["python", "src/app.py"]
CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:5000"]
