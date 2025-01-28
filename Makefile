# Tarea para instalar las dependencias del proyecto
install:
	python3 -m pip install -r requirements.txt

# Tarea para ejecutar los tests del proyecto
test:
	pytest --cov=src tests/

# Tarea para verificar el estilo del código
lint:
	flake8 proyecto_cc tests

# Tarea para limpiar archivos temporales
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
