# Problemas encontrados

## Hito 5
Durante el proceso de configuración, he tenido problemas relacionados con la falta de ciertas dependencias, como `python-dotenv`, que no estaban incluidas en el archivo `requirements.txt` inicial. Lo que ha hecho que apareciese un error de importación cuando la aplicación intentaba cargar las variables de entorno, y ha resultado en un fallo del despliegue. 


El problema lo he resuelto añadiendo el paquete a `requirements.txt`, haciendo `commit` de los cambios y luego forzando el despliegue manualmente en Render.