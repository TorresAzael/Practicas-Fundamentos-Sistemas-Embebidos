import threading
from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0X27)

def getTempRoom():
	while True:
		try:
			PathTemp = open("/sys/bus/w1/devices/28-19411e356461/temperature","r")
			tempVar = PathTemp.read()
			temp = float(tempVar)/1000
			lcd.cursor_pos = (1,1)
			lcd.write_string("Temp. {Cent} C  " .format(Cent=temp))
			sleep(1)
		except KeyboardInterrupt:
			return
def NamePrint():
	lcd.cursor_pos = (0, 0)
	lcd.write_string('Torres Anguiano')

def main():
	hilo1 = threading.Thread(target=getTempRoom)
	hilo2 = threading.Thread(target=NamePrint)
	hilo1.start()
	hilo2.start()
if __name__ == '__main__':
	main()
