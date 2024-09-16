# Gestión de Datos y Envío de Correos Electrónicos

Este proyecto está diseñado para gestionar datos de una base de datos SQLite, generar informes en formato CSV, crear archivos ZIP con los informes, y enviar correos electrónicos con los informes adjuntos. 

## Estructura del Proyecto

1. **`sqlManager.py`**: Contiene la clase `SQLDatabaseManager` para gestionar la conexión y operaciones con la base de datos SQLite.
2. **`fileManager.py`**: Contiene la clase `FileManager` para exportar datos de comercios a archivos CSV y crear archivos ZIP con los informes.
3. **`emailManager.py`**: Contiene la clase `EmailManager` para leer una plantilla HTML y enviar correos electrónicos con los informes adjuntos.
4. **`main.py`**: Archivo principal que coordina el flujo de trabajo, desde la conexión a la base de datos hasta el envío de correos electrónicos.

## Requisitos
- IMPORTANTE! PARA EJECUTAR EL ARCHIVO DEBE AGREGAR LA BASE DE DATOS DE SQLITE3 EN LA RUTA Y DEBE CONTENER LA SIGUINETE ESTRUCTURA: recursos/database.sqlite (de lo contrario no funcionara la herramienta)
- Python 3.6 o superior
- Paquetes de Python:
  - `pandas`
  - `pywin32`
  - `zipfile` (incluido en la biblioteca estándar de Python)

## Instalación de Dependencias

Para instalar las dependencias necesarias, puedes usar `pip`. Ejecuta el siguiente comando:

```bash
pip install pandas pywin32
