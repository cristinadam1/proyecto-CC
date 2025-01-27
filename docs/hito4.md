# Hito 4
## Estructura del clúster de contenedores
El clúster de contenedores diseñado para este proyecto tiene como objetivo principal organizar y aislar cada componente de la aplicación. Esto permite que los diferentes servicios y dependencias puedan interactuar entre sí sin conflictos y facilita la escalabilidad y la portabilidad del sistema. A continuación, voy a explicar la estructura que he usado:

### Estructura general del clúster
El clúster está compuesto por varios contenedores, cada uno con una responsabilidad específica:

1. Contenedor principal (aplicación): ejecuta la lógica principal de la aplicación. Contiene todos los modelos y servicios necesarios para gestionar las diferentes funcionalidades del sistema. Se basa en el archivo `app.py`, que actúa como el punto de entrada para los diferentes endpoints de la API.
2. Contenedor de base de datos: almacena toda la información de la aplicación, como los datos relacionados con actividades, medicamentos, recetas, residentes y el bienestar. Utiliza el archivo `database.db` y está configurado como un volumen para garantizar la persistencia de los datos.
3. Contenedor de tests: se usa para ejecutar pruebas automáticas y verificar que los servicios, modelos y la integración del sistema funcionan correctamente.


Cada contenedor interactúa dentro de una red común definida en `docker-compose.yml`

## Configuración de cada uno de los contenedores que componen el clúster de contenedores
### Contenedor de la aplicación
Es el núcleo del sistema, se encarga de ejecutar la lógica principal de la API. Para su construcción, he elegido como imagen base `python:3.10-slim`. En este contenedor se incluyen todos los modelos y servicios necesarios para gestionar las funcionalidades de la aplicación:

1. Modelos: se encuentran en la carpeta `src/models/` e incluyen los archivos `activity.py`, `medication.py`, `prescription.py`, `resident.py` y `wellness.py`. Cada modelo define la estructura de las tablas de la base de datos y sus relaciones.
2. Servicios: están en la carpeta `src/services/` y son responsables de la lógica de negocio. Cada servicio (activity_service.py, medication_service.py, etc.) proporciona funciones para interactuar con los modelos y exponer las funcionalidades mediante la API.
3. API principal: el archivo app.py centraliza la creación de la aplicación Flask, la configuración de la base de datos y la exposición de los endpoints. Este archivo asegura que los diferentes servicios puedan ser accedidos y gestionados a través de rutas HTTP.

Este contenedor mapea el puerto interno `5000` del contenedor al puerto `5000` de la máquina anfitriona para que se pueda acceder a la API desde el exterior. 

### Contenedor de la base de datos
Sirve para almacenar y gestionar los datos que utiliza la aplicación. Para este propósito, he usado la imagen `sqlite:latest`.

El contenedor está configurado para usar el archivo `database.db` como la base de datos principal de la aplicación. Además, he configurado un volumen persistente para garantizar que los datos se conserven incluso si el contenedor se detiene o reinicia. Este volumen asegura que los datos almacenados, como actividades, medicamentos, recetas, residentes y bienestar, no se pierdan.

La configuración de este contenedor incluye su integración en una red común para que pueda interactuar con el contenedor de la aplicación. Esto permite que los modelos definidos en la aplicación se conecten a la base de datos y realicen las operaciones necesarias.

### Contenedor para pruebas
El contenedor de pruebas está dedicado a verificar que la aplicación funciona bien mediante pruebas automatizadas. Este contenedor utiliza la misma imagen base que el contenedor de la aplicación (`python:3.10-slim`) 

En este contenedor se ejecutan las pruebas que validan los modelos, servicios y la integración general del sistema. Estas pruebas están diseñadas para garantizar que los endpoints funcionen como se espera y que la lógica de negocio sea correcta.

El uso de un contenedor separado para las pruebas permite aislar este proceso del entorno de producción. Además, garantiza que los resultados de las pruebas sean reproducibles, ya que el contenedor siempre parte de un entorno limpio y controlado.

### Justificación del uso de contenedores base
La elección de imágenes base ligeras como `python:3.10-slim` y `sqlite:latest` tiene como objetivo optimizar el tamaño de los contenedores y reducir los tiempos de construcción. Estas imágenes se usan mucho y estn muy bien documentadas, lo que facilita su configuración y mantenimiento. Además, aseguran la compatibilidad con las dependencias del proyecto y proporcionan un entorno estable para ejecutar la aplicación, la base de datos y las pruebas.