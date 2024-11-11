import logging
import pandas as pd
import datetime
import keyboard
import serial
import time
import configparser
from database_manager import connect_and_initialize_db, save_to_database, close_connection

# Leer archivo de configuración
config = configparser.ConfigParser()
config.read('config.ini')

# Acceder a los parámetros de configuración
serial_port = config['serial']['port']
baudrate = int(config['serial']['baudrate'])
check_interval = int(config['settings']['check_interval'])

# Configurar el puerto serial (ajustar según sea necesario)
ser = serial.Serial(serial_port, baudrate)

# Inicializar el dataframe
df = pd.DataFrame(columns=['FechaHora', 'Temperatura'])

def main():
    conn = connect_and_initialize_db()
    cursor = conn.cursor()
    start_time = time.time()

    while True:
        if keyboard.is_pressed('space'):
            logging.info("Ejecución detenida por el usuario.")
            break

        # Leer valor desde el puerto serial
        if ser.in_waiting > 0:
            temp_value = ser.readline().decode('utf-8').strip()
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.loc[len(df)] = [current_time, float(temp_value)]
            logging.info(f"Valor recibido: {temp_value} a las {current_time}")

        # Guardar cada check_interval segundos los últimos 10 valores
        if time.time() - start_time >= check_interval:
            save_to_database(cursor, df.tail(10))
            conn.commit()
            start_time = time.time()

        # Esperar un segundo antes de la siguiente lectura
        time.sleep(1)

    close_connection(conn)

if __name__ == "__main__":
    main()
