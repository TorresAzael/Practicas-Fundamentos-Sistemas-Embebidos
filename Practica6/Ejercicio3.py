#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ... [Encabezado omitido] ...

import smbus2
import struct
import time
import matplotlib.pyplot as plt
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

# RP2040 I2C device address
SLAVE_ADDR = 0x0A # I2C Address of RP2040

# Name of the file in which the log is kept
LOG_FILE = './temp.log'
GRAPH_FILE = './temp_graph.png'
HTML_PAGE = './index.html'
HOST_NAME = '0.0.0.0' # Para escuchar en todas las interfaces
PORT = 8000

# Initialize the I2C bus;
i2c = smbus2.SMBus(1)

# [Funciones readTemperature() y read_Date_Today() se mantienen iguales]
def readTemperature():
	# ... [Copia la función readTemperature() de Ejercicio2.py aquí] ...
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write (read request)
		data = list(msg)   # Converts stream to list
		ba = bytearray()
		for c in data:
			ba.append(int(c))
		temp = struct.unpack('<f',ba)
		temp = round(temp[0],2)
		return temp
	except:
		return None

def read_Date_Today():
	try:
		fecha = datetime.now()
		return fecha
	except:
		return None
# -------------------------------------------------------------------

def log_temp_date(temperature, date):
	if temperature is None or date is None:
		return
	try:
		# *** MODIFICACIÓN CLAVE: Se registra la fecha completa (ISO-like) para resolución de 1 minuto ***
		# Formato de registro: temperatura,YYYY-MM-DD HH:MM:SS
		log_entry = '{},{} \n'.format(temperature, date.strftime('%Y-%m-%d %H:%M:%S'))
		with open(LOG_FILE, "a") as fp:
			fp.write(log_entry)
	except Exception as e:
		print(f"Error al escribir en el log: {e}")

def generate_graph():
	"""Lee el log, filtra a resolución de 1 minuto, y genera el archivo de imagen."""
	dates = []
	temps = []
	last_minute = None

	try:
		with open(LOG_FILE, 'r') as logfile:
			for line in logfile:
				parts = line.strip().split(',')
				if len(parts) == 2:
					try:
						temp = float(parts[0].strip())
						# Analiza la fecha completa
						dt = datetime.strptime(parts[1].strip(), '%Y-%m-%d %H:%M:%S')
						
						# Filtro de resolución de 1 minuto: solo toma la primera lectura de cada minuto
						current_minute = dt.strftime('%Y-%m-%d %H:%M')
						if current_minute != last_minute:
							temps.append(temp)
							dates.append(dt)
							last_minute = current_minute
							
					except ValueError:
						continue # Ignorar líneas mal formadas o conversiones fallidas
		
		if temps:
			plt.figure(figsize=(12, 6))
			plt.plot(dates, temps, marker='o', linestyle='-', color='red')
			plt.title('Temperatura Histórica (Resolución de 1 minuto)')
			plt.xlabel('Fecha y Hora')
			plt.ylabel('Temperatura (°C)')
			plt.xticks(rotation=45, ha='right')
			plt.grid(True)
			plt.tight_layout()
			
			# Guardar la gráfica como un archivo PNG
			plt.savefig(GRAPH_FILE)
			plt.close() # Cierra la figura para liberar memoria
			return True
		else:
			print("No hay datos suficientes para generar el gráfico.")
			return False

	except FileNotFoundError:
		print(f"Archivo de log '{LOG_FILE}' no encontrado. Creando uno vacío.")
		open(LOG_FILE, 'a').close() # Crea el archivo si no existe
		return False
	except Exception as e:
		print(f"Error al generar el gráfico: {e}")
		return False

def create_html_page():
	"""Crea la página HTML simple para mostrar la imagen del gráfico."""
	html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="5"> <title>Monitor de Temperatura I2C</title>
</head>
<body>
    <h1>Gráfico de Temperatura Histórica (RPi I2C)</h1>
    <p>Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <img src="{os.path.basename(GRAPH_FILE)}" alt="Gráfico de Temperatura" style="max-width: 100%; height: auto;">
</body>
</html>
"""
	with open(HTML_PAGE, "w") as f:
		f.write(html_content)

def run_server():
	"""Configura y ejecuta el servidor web simple."""
	try:
		server_address = (HOST_NAME, PORT)
		httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
		print(f"Servidor web iniciado en http://{HOST_NAME}:{PORT}")
		print("Presione Ctrl+C para detener.")
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("Servidor web detenido.")
		httpd.server_close()
	except Exception as e:
		print(f"Error del servidor: {e}")

def main_web():
	"""Función principal modificada para lectura, log, generación de gráfica y servicio web."""
	# Inicia la recolección de datos y la generación de la gráfica en un bucle separado
	# Idealmente, esto debería correr en un hilo/proceso diferente al servidor web.
	# Por simplicidad, el servidor web se ejecutará después de una pausa para tener datos iniciales,
	# y un bucle de fondo se encargará de actualizar el log y la gráfica.
	
	print("Iniciando recolección de datos...")
	# Bucle para recoger 60 muestras (1 minuto inicial)
	for _ in range(60):
		try:
			cTemp = readTemperature()
			tDate = read_Date_Today()
			log_temp_date(cTemp, tDate)
			# print(f"Dato recolectado: {cTemp}")
			time.sleep(1)
		except KeyboardInterrupt:
			print("Recolección interrumpida.")
			return

	print("Generando gráfico inicial...")
	generate_graph()
	create_html_page()
	
	# Ejecutar el servidor web en el hilo principal
	run_server()

# Si se quiere ejecutar el servidor y la recolección continuamente en paralelo,
# se necesita usar el módulo 'threading'.
import threading

def data_collector_loop():
	"""Bucle continuo para leer, loguear y generar el gráfico."""
	while True:
		try:
			cTemp = readTemperature()
			tDate = read_Date_Today()
			
			log_temp_date(cTemp, tDate)
			# print(f"Lectura: {cTemp} @ {tDate.strftime('%H:%M:%S')}")

			# Generar la gráfica cada 30 segundos, por ejemplo, para limitar el I/O
			if tDate.second % 30 == 0:
				generate_graph()
				create_html_page() # Actualiza el timestamp en la página
				
			time.sleep(1)
		except Exception as e:
			print(f"Error en el bucle de datos: {e}")
			time.sleep(5) # Esperar antes de reintentar


def main():
	# Hilo para la recolección de datos y generación de gráficos
	collector_thread = threading.Thread(target=data_collector_loop, daemon=True)
	collector_thread.start()
	
	# Esperar un tiempo para que se generen datos iniciales
	time.sleep(5)
	
	# Generar el archivo HTML y ejecutar el servidor web
	create_html_page()
	run_server()

if __name__ == '__main__':
	main()