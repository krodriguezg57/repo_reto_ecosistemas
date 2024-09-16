import pandas as pd
import sqlite3

class SQLDatabaseManager:
    """
    Manejador para interactuar con una base de datos SQLite.
    """

    def __init__(self, db_path):
        """
        Inicializa la clase con la configuración de la base de datos.

        Args:
            db_path (str): Ruta al archivo de base de datos SQLite.
            conn (sqlite3.Connection): Conexión a la base de datos.
            cursor (sqlite3.Cursor): Cursor de la base de datos.
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Establece una conexión con la base de datos SQLite.
        
        Raises:
            sqlite3.Error: Si ocurre un error al conectar a la base de datos.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos establecida.")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def execute_sql_script(self, file_path):
        """
        Ejecuta un script SQL desde un archivo.

        Args:
            file_path (str): Ruta al archivo SQL.

        Raises:
            FileNotFoundError: Si el archivo SQL no se encuentra.
            sqlite3.Error: Si ocurre un error al ejecutar el script SQL.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as archivo_sql:
                sql_script = archivo_sql.read()
            self.cursor.executescript(sql_script)
            self.conn.commit()
            print("Script SQL ejecutado correctamente.")
        except FileNotFoundError:
            print(f"El archivo {file_path} no se encuentra.")
            raise
        except sqlite3.Error as e:
            print(f"Error al ejecutar el script SQL: {e}")
            self.conn.rollback()
            raise

    def read_data(self, query):
        """
        Lee datos de la base de datos usando una consulta SQL.

        Args:
            query (str): Consulta SQL para leer datos.

        Returns:
            pd.DataFrame: DataFrame con los datos leídos.

        Raises:
            Exception: Si ocurre un error al leer los datos.
        """
        try:
            df = pd.read_sql_query(query, self.conn)
            if df is not None and not df.empty:
                return df
            else:
                print("No se devolvieron datos.")
                return pd.DataFrame()  # Retorna un DataFrame vacío si no hay datos
        except Exception as e:
            print(f"Error al leer los datos: {e}")
            raise

    def close(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")