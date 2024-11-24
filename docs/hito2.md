# Memoria del hito 2
## Preparación del Entorno
En primer lugar he preparado mi entorno de desarrollo, clonando el repositorio desde GitHub a mi máquina local. Luego, he creado un entorno virtual para gestionar las dependencias del proyecto de manera aislada y evitar conflictos con otras bibliotecas que pudieran estar instaladas en mi sistema.
### Clonación del repositorio
    git clone https://github.com/usuario/proyecto-CC.git
    cd proyecto-CC
### Creación y activación del entorno virtual
Para crear el entorno virtual, he ejecutado el siguiente comando en la terminal

    python3 -m venv venv
    source venv/bin/activate
Esto ha activdo el entorno virtual, para que cualquier paquete que instale no afectare a mi sistema global

### Configuración de .gitignore
A continuación, he generado un archivo .gitignore para asegurarme de que los archivos temporales y el entorno virtual no se suban al repositorio
    
    touch .gitignore
    echo "venv/" >> .gitignore
    git add .gitignore
    git commit -m "Añadir .gitignore"

### Creación del Token de GitHub
Para poder hacer un git pull o git push desde mi entorno local, he creado un token personal de GitHub para poder autenticarme de manera segura y gestionar mis cambios en el repositorio
### Instalación de GitLens
He instalado la extensión GitLens en Visual Studio Code para gestionar el control de versiones de manera más eficiente y obtener una visualización más clara de los cambios en mi repositorio.


