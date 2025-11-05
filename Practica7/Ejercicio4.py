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
			tempFahr = round((temp*1.8) + 32,2)
			lcd.cursor_pos = (1,0)
			lcd.write_string("{Cent}C" .format(Cent=temp))
			lcd.cursor_pos = (1,7)
			lcd.write_string(' {Fahren}F'.format(Fahren=tempFahr) )
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
