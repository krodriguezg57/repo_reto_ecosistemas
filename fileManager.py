import zipfile
import os


class FileManager:
    """
    Manejador de archivos para exportar datos de la base de datos a archivos CSV y comprimirlos en archivos ZIP.

    Attributes:
        db_manager (SQLDatabaseManager): Instancia del manejador de base de datos SQL.
        report_dir (str): Directorio para guardar los archivos de reporte.
    """
    def __init__(self, db_manager, report_dir='./recursos/reportes'):
        """
        Inicializa la clase con un manejador de base de datos y el directorio para los reportes.

        Args:
            db_manager (SQLDatabaseManager): Instancia de SQLDatabaseManager para realizar consultas a la base de datos.
            report_dir (str): Directorio para guardar los archivos de reporte. Por defecto es './recursos/reportes'.

        Raises:
            ValueError: Si el directorio para guardar los reportes no es válido.
        """
        self.db_manager = db_manager
        self.report_dir = report_dir

    def export_commerce_data(self):
        """
        Exporta las transacciones y la facturación de cada comercio a archivos CSV.

        Este método obtiene una lista de comercios y crea dos archivos CSV para cada comercio:
        uno para las transacciones y otro para la facturación. Los archivos se guardan en el directorio
        especificado por `report_dir`.

        Raises:
            Exception: Si ocurre un error al leer datos de la base de datos o al guardar los archivos CSV.
        """
        # Obtén la lista de comercios
        comercios_query = "SELECT DISTINCT commerce_nit FROM temp_comercios_trx;"
        comercios_df = self.db_manager.read_data(comercios_query)

        if comercios_df.empty:
            print("No se encontraron comercios.")
            return

        # Exporta las transacciones y facturación de cada comercio a archivos CSV separados
        for comercio in comercios_df['commerce_nit']:
            # Exporta las transacciones
            query = f"SELECT * FROM temp_comercios_trx WHERE commerce_nit = '{comercio}';"
            df_transacciones = self.db_manager.read_data(query)
            df_transacciones.to_csv(f'{self.report_dir}/{comercio}_transacciones.csv', index=False)

            # Exporta la facturación
            query = f"SELECT * FROM tblfacturacion WHERE commerce_nit = '{comercio}';"
            df_facturacion = self.db_manager.read_data(query)
            df_facturacion.to_csv(f'{self.report_dir}/{comercio}_facturacion.csv', index=False)

    def create_zip_reports(self):
        """
        Crea archivos ZIP con los reportes de facturación y transacciones para cada comercio.

        Este método crea un archivo ZIP para cada comercio que contiene los archivos CSV de
        facturación y transacciones. Los archivos ZIP se guardan en el directorio especificado por `report_dir`.
        Después de crear el archivo ZIP, los archivos CSV individuales se eliminan.

        Raises:
            Exception: Si ocurre un error al leer datos de la base de datos, al crear el archivo ZIP, o al eliminar los archivos CSV.
        """
        # Lee el DataFrame de comercios para crear archivos ZIP
        comercios_query = "SELECT DISTINCT commerce_nit FROM temp_comercios_trx;"
        comercios_df = self.db_manager.read_data(comercios_query)

        if comercios_df.empty:
            print("No se encontraron comercios para crear archivos ZIP.")
            return

        # Crear archivos ZIP para cada comercio
        for _, row in comercios_df.iterrows():
            comercio = row['commerce_nit']
            reporte_factu = f'{self.report_dir}/{comercio}_facturacion.csv'
            reporte_trx = f'{self.report_dir}/{comercio}_transacciones.csv'
            archivo_zip = f'{self.report_dir}/{comercio}.zip'

            # Eliminar el archivo ZIP si ya existe
            if os.path.exists(archivo_zip):
                os.remove(archivo_zip)

            # Crear un archivo ZIP y agregar los archivos CSV
            with zipfile.ZipFile(archivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.exists(reporte_factu):
                    zipf.write(reporte_factu, os.path.basename(reporte_factu))
                if os.path.exists(reporte_trx):
                    zipf.write(reporte_trx, os.path.basename(reporte_trx))

            # Eliminar archivos CSV después de crear el ZIP
            if os.path.exists(reporte_factu):
                os.remove(reporte_factu)
            if os.path.exists(reporte_trx):
                os.remove(reporte_trx)