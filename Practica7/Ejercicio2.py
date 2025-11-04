from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0X27)

def NamePrint():
	lcd.cursor_pos = (0, 0)
	lcd.write_string('Torres Anguiano')
NamePrint()
