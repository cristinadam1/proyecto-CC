# Análisis del dominio del problema
## Entidades del Dominio del Problema
### Residente:
Representa a una persona que recibe atención y tiene un horario de medicamentos asignado.
- Identificador (ID): Código único que identifica al residente.
- Nombre: Nombre del residente.
- Edad: Edad del residente.
- Horario de medicamentos: Lista de medicamentos y sus horarios.

### Medicamento:
Representa un medicamento que debe ser administrado a un residente.
- Identificador (ID): Código único del medicamento.
- Nombre: Nombre del medicamento.
- Dosis: Cantidad de medicamento que debe tomarse.
- Frecuencia: Veces al día o semana que se toma el medicamento.

### Horario de Medicación:
Define cuándo y qué medicamento debe tomar un residente.
- Identificador (ID): Código único del horario.
- Residente: Referencia al residente asociado.
- Medicamento: Referencia al medicamento asociado.
- Hora: Hora exacta en la que se toma el medicamento.

### Reporte de Medicación:
Documento que permite llevar un registro del cumplimiento del tratamiento.
- Identificador (ID): Código único del reporte.
- Residente: Referencia al residente.
- Fecha: Día en el que se generó el reporte.
- Medicamentos tomados: Lista de medicamentos tomados.
- Observaciones: Notas adicionales sobre el estado del residente.

## Relaciones entre Entidades
Un residente tiene varios medicamentos asignados.
Un medicamento puede ser tomado por varios residentes.
Cada horario de medicación pertenece a un único residente y a un único medicamento.
Los reportes de medicación se generan para un residente y contienen información sobre los medicamentos tomados.