import os
from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574',0x27)

def getTempRoom():
	PathTemp = open("/sys/bus/w1/devices/28-19411e356461/temperature","r")
	tempVar = PathTemp.read()
	temp = float(tempVar)/1000
	lcd.cursor_pos = (0,1)
	lcd.write_string("Temp. {Cent} C" .format(Cent=temp))
getTempRoom()

def main():
	while True:
		try:
			getTempRoom()
			sleep(1)
			lcd.clear()
		except KeyboardInterrupt:
			return
if __name__ == '__main__':
 	main()
