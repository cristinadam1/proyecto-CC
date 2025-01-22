# Arquitectura 
## Microservicios
### Resident-Manager:
Este microservicio es el núcleo del sistema y se encargará de administrar la información de los residentes y sus horarios de medicación. Sus funcionalidades principales serán:
1. Gestión de residentes:
- Crear nuevos residentes.
- Modificar los datos básicos de los residentes, como nombre o edad.
- Eliminar residentes del sistema.
2. Gestión de horarios de medicación:
- Asignar medicamentos a los residentes con horarios y dosis específicos.
- Actualizar los horarios y las dosis de los medicamentos asignados.
- Eliminar medicamentos de los horarios de un residente.

### Medication-Manager:
Este microservicio gestionará la base de datos de medicamentos disponibles. Sus funcionalidades serán:
1. Gestión de medicamentos:
- Registrar nuevos medicamentos con información como dosis estándar, nombre y descripción.
- Modificar los detalles de medicamentos existentes.
- Eliminar medicamentos que ya no estén disponibles o que hayan sido reemplazados.

### Adherence-Manager:
Este microservicio se encargará de realizar un seguimiento de la adherencia de los residentes a sus tratamientos y generar métricas relevantes. Sus funcionalidades incluirán:
1. Seguimiento de adherencia:
- Calcular el porcentaje de cumplimiento del horario de medicación para cada residente.
- Registrar eventos de omisión o retraso en la toma de medicamentos.
2. Generación de alertas:
- Enviar notificaciones en caso de que un residente esté incumpliendo con su tratamiento.

### Report-Manager:
Este microservicio generará reportes detallados para la supervisión y análisis. Funcionalidades principales:
1. Generación de reportes personalizados:
- Informes de adherencia por residente o por un grupo específico.
- Historial completo de medicamentos asignados y tomados.
2. Historial de reportes:
- Consultar y almacenar reportes previamente generados.

## Servicios
- Sistema de Logs.
- API Gateway.
- Sistema de configuración distribuida.

## Bases de datos
1. Base de datos de residentes y horarios de medicación: almacena información básica sobre los residentes y sus horarios de medicación.
- residentes: ID, nombre, edad, contacto.
- medicamentos: ID, nombre, dosis estándar, frecuencia.
- horarios: ID, residente_id, medicamento_id, hora, frecuencia, estado (tomado/no tomado).

2. Base de datos de reportes y adherencia: contiene los reportes generados y las métricas de adherencia.
- reportes: ID, residente_id, medicamentos_tomados, fecha, observaciones.
- estadisticas: ID, residente_id, porcentaje_cumplimiento, alertas_generadas