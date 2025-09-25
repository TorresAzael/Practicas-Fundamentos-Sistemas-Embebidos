# !/usr/bin/env python3
# ## ###############################################
#
# led_manager.py
# Controls leds in the GPIO
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################
import RPi.GPIO as GPIO
from time import sleep

"Definicion de las salidas de leds"
GPIO.setmode(GPIO.BOARD)
NumLeds = [12,16,18,22,24,26,32]
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

"Inicializamos los leds"
for i in range(len(NumLeds)):
  GPIO.setup(NumLeds[i], GPIO.OUT, initial=GPIO.LOW)

""" Enciende el leds especificados en num, apagando los demás
	(To be developed by the student)
"""
def leds(num):
	GPIO.output(NumLeds[num], GPIO.HIGH)
	sleep(0.5)
	GPIO.output(NumLeds[num], GPIO.LOW)

""" Activa el modo marquesina
	type toma tres valores: left, right y pingpong
	(To be developed by the student)
"""
def marquee(type='pingpong'):
	switcher = {
		'left'     : _marquee_left,
		'right'    : _marquee_right,
		'pingpong' : _marquee_pingpong
	}
	func = switcher.get(type, None)
	if func:
		func()


"""	Despliega en número proporcionado en el display de siete segmentos.
	(To be developed by the student)
"""
def bcd(num):
	GPIO.output(36, GPIO.HIGH if (num & 0x00000001) > 0 else GPIO.LOW )
	GPIO.output(38, GPIO.HIGH if (num & 0x00000002) > 0 else GPIO.LOW )
	GPIO.output(40, GPIO.HIGH if (num & 0x00000004) > 0 else GPIO.LOW )
	GPIO.output(37, GPIO.HIGH if (num & 0x00000008) > 0 else GPIO.LOW )

""" Activa el modo marquesina continua a la izquierda"""
def _marquee_left():
	i=0
	FinalLoop=True
	while FinalLoop:
	  GPIO.output(NumLeds[i],GPIO.HIGH)
	  sleep(0.1)
	  GPIO.output(NumLeds[i],GPIO.LOW)
	  i+=1
	  if(i>=7):
	    i=0
	    FinalLoop=False
	for i in range(6):
	  GPIO.output(NumLeds[i],GPIO.LOW)
""" Activa el modo marquesina continua a la derecha"""
def _marquee_right():
	i=6
	FinalLoop=True
	while FinalLoop:
	  GPIO.output(NumLeds[i],GPIO.HIGH)
	  sleep(0.1)
	  GPIO.output(NumLeds[i],GPIO.LOW)
	  i-=1
	  if(i<=-1):
	    i=6
	    FinalLoop=False
	for i in range(6):
	  GPIO.output(NumLeds[i],GPIO.LOW)
""" Activa el modo marquesina ping-pong"""
def _marquee_pingpong():
	i=0
	j=6
	bandera=0
	FinalLoop=True
	while FinalLoop:
	    if(bandera==0):
	      GPIO.output(NumLeds[i], GPIO.HIGH)
	      sleep(0.1)
	      GPIO.output(NumLeds[i], GPIO.LOW)
	      i+=1
	    if(bandera==1):
	      GPIO.output(NumLeds[j], GPIO.HIGH)
	      sleep(0.1)
	      GPIO.output(NumLeds[j], GPIO.LOW)
	      j-=1
	    if(i>=7):
	      i=0
	      bandera=1
	    if(j==0):
	      j=6
	      bandera=0
	      FinalLoop=False
	    if(FinalLoop==False):
	      for i in range(6):
	        GPIO.output(NumLeds[i],GPIO.LOW)
