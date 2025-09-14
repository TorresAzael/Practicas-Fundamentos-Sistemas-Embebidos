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
# Configurar el pin 32 como salida y habilitar en bajo
for i in range(len(leds)):
  GPIO.setup(leds[i], GPIO.OUT, initial=GPIO.LOW)

# El siguiente código hace parpadear el led
while True: # Bucle infinito
	sleep(0.5)                 # Espera 500ms
	GPIO.output(12, GPIO.HIGH) # Enciende el led
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(18, GPIO.HIGH)
	GPIO.output(22, GPIO.HIGH)
	GPIO.output(24, GPIO.HIGH)
	GPIO.output(26, GPIO.HIGH)
	GPIO.output(32, GPIO.HIGH)
	sleep(0.5)                 # Espera 500ms
	GPIO.output(12, GPIO.LOW)  # Apaga el led
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(24, GPIO.LOW)
	GPIO.output(26, GPIO.LOW)
	GPIO.output(32, GPIO.LOW)
