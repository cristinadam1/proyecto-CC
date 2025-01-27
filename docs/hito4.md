# Hito 4
## Estructura del clúster de contenedores
El clúster de contenedores diseñado para este proyecto tiene como objetivo principal organizar y aislar cada componente de la aplicación. Esto permite que los diferentes servicios y dependencias puedan interactuar entre sí sin conflictos y facilita la escalabilidad y la portabilidad del sistema. A continuación, voy a explicar la estructura que he usado:

### Estructura general del clúster
El clúster está compuesto por varios contenedores, cada uno con una responsabilidad específica:

1. Contenedor principal (aplicación): ejecuta la lógica principal de la aplicación. Contiene todos los modelos y servicios necesarios para gestionar las diferentes funcionalidades del sistema. Se basa en el archivo `app.py`, que actúa como el punto de entrada para los diferentes endpoints de la API.
2. Contenedor de base de datos: almacena toda la información de la aplicación, como los datos relacionados con actividades, medicamentos, recetas, residentes y el bienestar. Utiliza el archivo `database.db` y está configurado como un volumen para garantizar la persistencia de los datos.
3. Contenedor de tests: se usa para ejecutar pruebas automáticas y verificar que los servicios, modelos y la integración del sistema funcionan correctamente.

## Componentes incluidos en el contenedor de la aplicación
El contenedor de la aplicación incluye las siguientes rutas y funcionalidades:

1. Modelos: se encuentran en la carpeta `src/models/` e incluyen los archivos `activity.py`, `medication.py`, `prescription.py`, `resident.py` y `wellness.py`. Cada modelo define la estructura de las tablas de la base de datos y sus relaciones.
2. Servicios: están en la carpeta `src/services/` y son responsables de la lógica de negocio. Cada servicio (activity_service.py, medication_service.py, etc.) proporciona funciones para interactuar con los modelos y exponer las funcionalidades mediante la API.
3. API principal: el archivo app.py centraliza la creación de la aplicación Flask, la configuración de la base de datos y la exposición de los endpoints. Este archivo asegura que los diferentes servicios puedan ser accedidos y gestionados a través de rutas HTTP.

Cada contenedor interactúa dentro de una red común definida en `docker-compose.yml`

## Configuración de cada uno de los contenedores que componen el clúster de contenedores