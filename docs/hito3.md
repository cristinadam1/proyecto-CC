# Hito 3
# Hito 3: Diseño de Microservicios

## Introducción
En este hito, he desarrollado un microservicio basado en la funcionalidad que había implementado en el [hito 2]("hito2")
He hecho lo siguiente:
- Diseñar una API REST con rutas consistentes.
- Añadir un sistema de logs para registrar la actividad de la API.
- Testear la API.
- Probar las rutas usando Postman.

## Justificación técnica del framework elegido para el microservicio
He elegido Flask como framework para desarrollar mi microservicio porque es bastante sencillo de usar y ligero, lo cual me viene muy bien para implementar la API REST que permita gestionar los residentes. Además, tiene con una comunidad grande y buena documentación, lo que facilita encontrar soluciones si surge algún problema.

Otro punto importante es que Flask tiene extensiones que se pueden añadir fácilmente para cosas más avanzadas, como autenticación o manejo de bases de datos, si en el futuro quiero ampliar el proyecto. Pero para este hito, que requiere crear rutas REST simples y manejar peticiones, Flask es perfecto porque ya incluye todo lo necesario sin ser complicado.

## Diseño de la API

- **POST `/add_resident`**: Añade un nuevo residente.
  - Parámetros: JSON con `name` (string), `age` (int) y `contact` (string).
  - Respuesta: ID del residente creado.
- **PUT `/update_resident/<int:resident_id>`**: Actualiza los datos de un residente existente.
  - Parámetros: ID del residente en la URL y JSON con los campos a actualizar.
  - Respuesta: Mensaje de éxito o error.
- **DELETE `/remove_resident/<int:resident_id>`**: Elimina un residente específico.
  - Parámetros: ID del residente en la URL.
  - Respuesta: Mensaje de éxito o error.
- **GET `/get_residents`**: Recupera la lista de residentes.
  - Respuesta: JSON con la lista completa de residentes.

### Separación de capas
En el diseño, me he asegurado de que la API no tenga lógica de negocio. La lógica, como agregar o actualizar residentes, está en la clase ResidentManager. La API simplemente llama a los métodos de esta clase. Por ejemplo:

- Cuando alguien hace una solicitud para añadir un residente, la API toma los datos de la solicitud y los pasa al método add_resident de ResidentManager.
- Si hay un error, como intentar eliminar un residente que no existe, ResidentManager maneja ese error, y la API se encarga de devolver una respuesta adecuada.

### Uso de Postman
Para verificar que la API funcionaba bien he usado **Postman** para realizar pruebas manuales. Con Postman he enviado solicitudes HTTP a cada una de las rutas, comprobando:
1. El correcto manejo de las peticiones válidas.
2. La gestión de errores, como intentar actualizar o eliminar un residente que no existe.

Con esto he podido visualizar las respuestas en tiempo real y asegurarme de que los datos que devuelve la API son correctos.

## Sistema de Logs
He implementado un sistema de logs para registrar toda la actividad que ocurre en la API, cada vez que alguien utiliza una ruta, se genera un mensaje que guarda información importante sobre lo que pasó. Por ejemplo, cuando se añade un residente, el log guarda un mensaje diciendo que un nuevo residente fue añadido y muestra su información. Si ocurre un error, como intentar borrar un residente que no existe, también se guarda un mensaje explicando el problema.
He usado la biblioteca estándar de Python `logging`. La configuración incluye:
- Registro en consola con el nivel de severidad `INFO` y `ERROR`.
- Mensajes descriptivos que detallan cada operación 

### Ejemplos de Logs
- Al añadir un residente:
  ```plaintext
  2025-01-23 12:34:56,123 - INFO - Added resident: {'id': 1, 'name': 'Silvia Martin', 'age': 70, 'contact': '609690502'}

