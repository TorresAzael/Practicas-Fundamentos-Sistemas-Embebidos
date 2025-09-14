#!/usr/bin/env python3
# ## ###############################################
#
# pwm.py
# Blinks a led on pin 32 using Raspberry Pi's PWM
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
GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
GPIO.setmode(GPIO.BOARD)
# Configurar el pin 32 como salida y habilitar en bajo
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)
# Inicializar el pin 32 como PWM a una frecuencia de 1Hz
pwm = GPIO.PWM(32, 1000)

# El siguiente código hace parpadear el led
pwm.start(50)
flag = True
dutyCycle = [0,20,40,60,80,100]
i=0
while flag:
	pwm.ChangeDutyCycle(dutyCycle[i])
	i+=1
	sleep(0.1)
	if(i>=6):
	  i=0
	#end try
#end while
# Detiene el PWM
pwm.stop()
# Reinicia los puertos GPIO (cambian de salida a entrada)
GPIO.cleanup()

