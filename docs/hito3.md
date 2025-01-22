# Hito 3

## Marco elegido para el microservicio
Para la implementación del microservicio he usado utilizado Flask, por su simplicidad y flexibilidad, además de su compatibilidad con pruebas automatizadas y una curva de aprendizaje amigable.

## Diseño general de la API
### Diseño por capas
El microservicio se organiza en tres capas principales:

1. Capa de presentación (API): responsable de manejar las solicitudes HTTP. Define las rutas y traduce los datos en formato JSON para interactuar con la lógica de negocio.
    Herramienta usada: Flask.

2. Capa de lógica de negocio: implementa la funcionalidad principal de la aplicación. Aquí se encuentran las operaciones y reglas específicas de negocio.
    Archivo principal: logic.py

3. Capa de pruebas: asegura que tanto la lógica de negocio como las rutas de la API funcionen correctamente.
    Archivo de pruebas: tests/test_logic.py

Este diseño permite modificar la API o la lógica de negocio de manera independiente, mejorando la flexibilidad y mantenibilidad.
