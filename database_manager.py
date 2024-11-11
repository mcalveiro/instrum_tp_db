import sqlite3
import os
import logging
import configparser

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Leer archivo de configuración
config = configparser.ConfigParser()
config.read('config.ini')

# Acceder a los parámetros de configuración
db_name = config['database']['db_name']
table_name = config['database']['table_name']

# Ruta del archivo de la base de datos SQLite
db_path = os.path.join(os.path.dirname(__file__), db_name)

# Conectar a la base de datos SQLite y crear tabla si no existe
def connect_and_initialize_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            FechaHora DATETIME,
            Temperatura FLOAT
        )
    """)
    conn.commit()
    return conn

# Guardar los datos en la base de datos
def save_to_database(cursor, df):
    for _, row in df.iterrows():
        cursor.execute(f"INSERT INTO {table_name} (FechaHora, Temperatura) VALUES (?, ?)", 
                       (row['FechaHora'], row['Temperatura']))
    logging.info("Datos guardados en la base de datos.")

def close_connection(conn):
    conn.close()
    logging.info("Conexión cerrada.")

if __name__ == "__main__":
    conn = connect_and_initialize_db()
    cursor = conn.cursor()
    # Aquí puedes agregar más operaciones de prueba o mantenimiento.
    close_connection(conn)
