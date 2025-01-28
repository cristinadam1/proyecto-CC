from flasgger import Swagger

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "SeniorCare",
        "description": "Documentación interactiva de la API",
        "version": "1.0.0"
    },
    "host": "localhost:5000",  
    "basePath": "/",
    "schemes": ["http", "https"],
}

def configure_swagger(app):
    """Configura Swagger en la aplicación Flask."""
    Swagger(app, template=swagger_template)

