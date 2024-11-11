import pandas as pd
import time
import configparser
import sqlite3
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Leer archivo de configuración
config = configparser.ConfigParser()
config.read('config_problems.ini')

# Acceder a los parámetros de configuración
db_name = config['database']['db_name']
table_name = config['database']['table_name']
event_table_name = config['database']['event_table_name']
alta_temperatura = float(config['settings']['alta_temperatura'])
muestra_consecutiva = int(config['settings']['muestra_consecutiva'])
check_interval = int(config['settings']['check_interval'])

# Ruta de la base de datos
db_path = os.path.join(os.path.dirname(__file__), db_name)

# Conectar y crear la tabla de eventos si no existe
def connect_and_initialize_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {event_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            FechaHora DATETIME,
            Temperatura FLOAT
        )
    """)
    conn.commit()
    return conn

# Monitorear temperaturas y registrar eventos de alta temperatura
def monitor_temperature(cursor):
    query = f"SELECT FechaHora, Temperatura FROM {table_name} ORDER BY FechaHora DESC LIMIT {muestra_consecutiva}"
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == muestra_consecutiva and all(float(row[1]) > alta_temperatura for row in results):
        logging.info(f"Umbral de alta temperatura superado durante {muestra_consecutiva} muestras consecutivas.")
        latest_entry = results[0]
        cursor.execute(f"INSERT INTO {event_table_name} (FechaHora, Temperatura) VALUES (?, ?)", latest_entry)
        logging.info("Evento de alta temperatura registrado en la base de datos.")

def main():
    conn = connect_and_initialize_db()
    cursor = conn.cursor()
    start_time = time.time()

    while True:
        if time.time() - start_time >= check_interval:
            monitor_temperature(cursor)
            conn.commit()
            start_time = time.time()

        time.sleep(1)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
