#!/usr/bin/env python3
# ## ###############################################
#
# pwm.py
# Blinks a led on pin 32 using Raspberry Pi
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

# Importa la librería de control del GPIO de la Raspberry Pi
import RPi.GPIO as GPIO
# Importa la función sleep del módulo time
from time import sleep

# Desactivar advertencias (warnings)
# GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
# Llame GPIO.setmode(GPIO.BCM) para usar el canal SOC definido por Broadcom
GPIO.setmode(GPIO.BOARD)
leds = [12,16,18,22,24,26,32]
i = 0
Flag = True
# Configurar el pin 32 como salida y habilitar en bajo
for i in range(len(leds)):
  GPIO.setup(leds[i], GPIO.OUT, initial=GPIO.LOW)

# El siguiente código hace parpadear el led
velocidad = int(input("Digite un numero entero: "))
mili=velocidad/100
while Flag: # Bucle infinito
	try:
	  #sleep(0.2)                 # Espera 500ms
	  GPIO.output(leds[i], GPIO.HIGH) # Enciende el led
	  sleep(mili)                 # Espera 500ms
	  GPIO.output(leds[i], GPIO.LOW)  # Apaga el led
	  i+=1
	  if(i>=7):
	    i =0
	except:
	  Flag = False
