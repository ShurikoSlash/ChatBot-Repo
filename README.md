TPI for OE - Programacion I - UTN
Chatbot de Gestión de Vacaciones

Descripción

Este proyecto consiste en un chatbot desarrollado en Python para automatizar el proceso de solicitud de vacaciones dentro de una empresa.

El sistema permite que un empleado consulte y solicite sus vacaciones mediante una conversación simple, validando la información ingresada y actualizando los días disponibles de forma automática.

Objetivo

Automatizar un proceso administrativo que normalmente se realiza de forma manual, reduciendo tiempos de gestión y minimizando errores humanos.

Tecnologías Utilizadas

- Python 3
- CSV como base de datos simulada
- GitHub para control de versiones

Archivos del Proyecto

Chatbot.py

Contiene toda la lógica del chatbot.

vacacionesDB.csv

Base de datos simulada de empleados.

Campos:

- legajo
- nombre
- dias_disponibles

solicitudes_log.csv

Registro histórico de solicitudes realizadas por los empleados.

Funcionalidades

- Validación de legajo.
- Consulta de días disponibles.
- Solicitud de vacaciones.
- Validación de fechas.
- Verificación de saldo disponible.
- Registro de solicitudes aprobadas y rechazadas.
- Actualización automática del saldo.

Ejecución

1. Abrir una terminal.
2. Ubicarse en la carpeta del proyecto.
3. Ejecutar:

python Chatbot.py

Flujo General

1. El usuario escribe "vacaciones".
2. El sistema solicita el número de legajo.
3. El sistema verifica la existencia del empleado.
4. Se solicitan fechas de inicio y fin.
5. El sistema calcula los días solicitados.
6. Se valida el saldo disponible.
7. La solicitud es aprobada o rechazada.
8. Se registra la operación.

Autor

Ezequiel Gómez

Trabajo Práctico Integrador

Organización Empresarial

Tecnicatura Universitaria en Programación a Distancia