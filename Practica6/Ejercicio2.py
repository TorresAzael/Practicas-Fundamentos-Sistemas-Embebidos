#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
#
# Author: Mauricio Matamoros
# Date:
#
# ## ############################################################
import smbus2
import struct
import time

import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os
# RP2040 I2C device address
SLAVE_ADDR = 0x0A # I2C Address of RP2040

# Name of the file in which the log is kept
LOG_FILE = './temp.txt'

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)
def readTemperature():
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write (read request)
		data = list(msg)   # Converts stream to list
		# list to array of bytes (required to decode)
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
		print('Problema con la fecha!!!\n')
		return None

def log_temp_date(temperature, date):
	try:
		with open(LOG_FILE, "a") as fp:
			fp.write('{},{}:{}:{} \n'.format(temperature, date.hour, date.minute, date.second))
	except:
		return

def graph_TempDate(Date):

	x = []
	y = []

	with open('temp.txt','r') as fp:
		plots = csv.reader(fp, delimiter=',')
		for row in plots:
			x.append(row[1])
			y.append(float(row[0]))

	plt.plot(x,y, label='Variación de la temperatura')
	plt.xlabel('Tiempo - Fecha De Hoy:{Dia}/{Mes}/{Año}'
			.format(Dia=Date.day,Mes=Date.month,Año=Date.year))
	plt.ylabel('Temperatura')
	plt.title('Gráfica Lectura de Temperatura con RP2040')
	plt.legend()
	plt.show()

def main():
	while True:
		try:
			cTemp = readTemperature()
			tDate = read_Date_Today()

			log_temp_date(cTemp, tDate)

			print('Temperatura recibida:{varTemp}°C,{varHrs}:{varMinu}:{varSeg}'
					.format(varTemp=cTemp, varHrs=tDate.hour, varMinu=tDate.minute,varSeg=tDate.second))
			time.sleep(1)

		except KeyboardInterrupt:
			graph_TempDate(tDate)
			os.remove('temp.txt')
			return

if __name__ == '__main__':
	main()
