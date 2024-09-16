from sqlManager import SQLDatabaseManager
from emailManager import EmailManager
from fileManager import FileManager
from datetime import date
import pandas as pd

def main():
    """
    Función principal para ejecutar el flujo de trabajo de gestión de datos y envío de correos.
    
    Esta función realiza las siguientes tareas:
    1. Configura las rutas de la base de datos, archivos SQL, directorio de reportes y archivo de plantilla HTML.
    2. Crea instancias de los manejadores de base de datos, archivos y correos.
    3. Conecta a la base de datos.
    4. Ejecuta los scripts SQL necesarios para preparar la base de datos.
    5. Exporta datos de comercios a archivos CSV y crea archivos ZIP con los reportes.
    6. Lee datos de facturación desde la base de datos y los guarda en un archivo CSV con fecha.
    7. Envia correos electrónicos con los informes adjuntos.
    
    El método `email_manager.enviar_correos(df)` espera que el DataFrame `df` contenga las columnas necesarias para personalizar los correos.
    
    Raises:
        Exception: Si ocurre un error en la conexión a la base de datos, ejecución de scripts SQL, exportación de datos, creación de archivos ZIP, lectura de datos o envío de correos.
    """
    # 1. Configuración Inicial
    db_path = "./recursos/database.sqlite"
    sql_file_path = ["./recursos/sql/temp_comercios_trx.sql", './recursos/sql/tblfacturacion.sql']
    report_dir = './recursos/reportes'
    ruta_archivo_html = "./recursos/plantilla.html"
    
    # 2. Creación de Instancias
    db_manager = SQLDatabaseManager(db_path)
    report_manager = FileManager(db_manager, report_dir)
    email_manager = EmailManager(ruta_archivo_html)  # Nueva instancia de EmailManager

    try:
        # 3. Conexión a la Base de Datos
        db_manager.connect()

        # 4. Ejecución de Scripts SQL
        for sql_file in sql_file_path:
            db_manager.execute_sql_script(sql_file)

        # 5. Exportación de Datos y Creación de Informes ZIP
        report_manager.export_commerce_data()
        report_manager.create_zip_reports()

        # 6. Lectura de Datos desde la Base de Datos
        consulta_sql = "SELECT * FROM tblfacturacion"  # Asegúrate de que esta tabla existe
        df = db_manager.read_data(consulta_sql)

        # Mostrar las primeras filas del DataFrame
        if not df.empty:
            print(df.head())
            fecha = date.today()
            # Formatear la fecha y hora en un formato específico
            fecha_formateada = fecha.strftime('%d%m%Y')
            csv_path = f'./recursos/{fecha_formateada}_facturacion_comercios.csv'
            df.to_csv(csv_path, index=False)

            # 7. Enviar Correos Electrónicos
            email_manager.enviar_correos(df)

    finally:
        # 8. Cierre de Conexión a la Base de Datos
        print("Gracias y Te quiero mucho <3")
        db_manager.close()

if __name__ == "__main__":
    main()
