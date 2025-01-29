# Hito 2

## Preparación del Entorno
En primer lugar he preparado mi entorno de desarrollo, clonando el repositorio desde GitHub a mi máquina local. Luego, he creado un entorno virtual para gestionar las dependencias del proyecto de manera aislada y evitar conflictos con otras bibliotecas que pudieran estar instaladas en mi sistema.
### 1. Clonación del repositorio
    git clone https://github.com/usuario/proyecto-CC.git
    cd proyecto-CC
    
### 2. Creación y activación del entorno virtual
Para crear el entorno virtual, he ejecutado el siguiente comando en la terminal

    python3 -m venv venv
    source venv/bin/activate
Esto ha activdo el entorno virtual, para que cualquier paquete que instale no afectare a mi sistema global

### 3. Configuración de .gitignore
A continuación, he generado un archivo .gitignore para asegurarme de que los archivos temporales y el entorno virtual no se suban al repositorio
    
    touch .gitignore
    echo "venv/" >> .gitignore
    git add .gitignore
    git commit -m "Añadir .gitignore"

### 4. Creación del Token de GitHub
Para poder hacer un git pull o git push desde mi entorno local, he creado un token personal de GitHub para poder autenticarme de manera segura y gestionar mis cambios en el repositorio

### 5. Instalación de GitLens
He instalado la extensión GitLens en Visual Studio Code para gestionar el control de versiones de manera más eficiente y obtener una visualización más clara de los cambios en mi repositorio.

## Elección y configuración del gestor de tareas
Una vez configurado el entorno, el siguiente paso es preparar el sistema para la ejecución de los tests mediante un gestor de tareas. He usado Makefile, ya que me era más conocida y es una herramienta muy útil para definir tareas repetitivas de manera sencilla.

### 1. Activación del Entorno Virtua
Si el entorno no estaba activo, lo activamos nuevamente con el siguiente comando

    source venv/bin/activate

### 2. Creación del Makefile
Creo un archivo Makefile en la raíz del proyecto para definir las tareas de gestión, como la instalación de dependencias y la ejecución de tests

Tarea para instalar las dependencias del proyecto
    
    install:
	    python3 -m pip install -r requirements.txt

Tarea para ejecutar los tests del proyecto

    test:
	    pytest --cov=proyecto_cc tests/

Tarea para verificar el estilo del código
    
    lint:
	    flake8 proyecto_cc tests

Tarea para limpiar archivos temporales

    clean:
	    find . -name '*.pyc' -delete
	    find . -name '__pycache__' -delete

### 3. Creación del archivo requirements.txt
Para listar las dependencias necesarias para el proyecto

    touch requirements.txt

## Elección de la biblioteca de aserciones
He decidido usar pytest como la biblioteca de aserciones para este proyecto por su simplicidad y flexibilidad. Además al ser de Python, voy a tener más documentación y soporte. Por otra parte, su sintaxis es fácil de entender y permite realizar pruebas unitarias, funcionales e incluso de integración de manera eficiente.

## Elección y uso del marco de pruebas
El marco de pruebas que he elegido es pytest, que se integra perfectamente con la biblioteca de aserciones mencionada anteriormente. pytest no solo ejecuta pruebas unitarias, sino que también permite organizar las pruebas de manera eficiente y proporciona una excelente salida en la terminal. Además, tiene soporte para la ejecución de pruebas de integración, lo que resulta útil a medida que el proyecto crece y se vuelve más complejo.

Para ejecutar las pruebas, he configurado el comando make test en el Makefile, que permite ejecutar pytest de manera automatizada y repetible.

## Integración continua funcionando y correcta justificación del sistema elegido
El siguiente paso ha sido configurar la integración continua para ejecutar automáticamente los tests cada vez que se haga un push a GitHub para asegurar que los cambios que haga en el código no rompan funcionalidades y que siempre se pase por el proceso de pruebas antes de desplegarse.

### 1. Creación de la estructura de directorios
Primero, he creado la estructura necesaria para los archivos de GitHub Actions

    mkdir -p .github/workflows
    git add .github/
    git commit -m "Crear estructura de directorios para GitHub Actions"

### 2. Creación del archivo de configuración
Luego, he creado el archivo .github/workflows/ci.yml con la configuración del flujo de trabajo de CI

    name: CI Pipeline
    
    on:
      push:
        branches:
          - main
      pull_request:
        branches:
          - main
    
    jobs:
      test:
        runs-on: ubuntu-latest

        steps:
        - name: Check out the code
          uses: actions/checkout@v3
    
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: 3.13
    
        - name: Install dependencies
          run: |
            python3 -m pip install --upgrade pip
            python3 -m pip install -r requirements.txt
    
        - name: Run tests
          run: |
            pytest --cov=src tests/

### 3. Actualización
Después de crear la configuración de GitHub Actions, hago un commit para subir la estructura y la configuración al repositorio
    
    git add .github/
    git commit -m "Create GitHub Actions folder structure"

Al hacer un push a mi repositorio en GitHub, la integración continua se activa automáticamente y ejecuta los tests que he definido. Cada vez que se hace un cambio, GitHub Actions verifica si el código funciona correctamente.

Para ejecutar los test usamos el comando:

    make test 

    


