# ## ################################################################
# blink.py
#
# Author:  Mauricio Matamoros
# License: MIT
#
# Reads the temperature of the RP2040 in Celcius
#
# ## ################################################################

from machine import ADC          # Board Analogic-to-Digital Converter
from utime import sleep_ms       # Delay function in milliseconds

def main():                      # Main function
    K = -0.029259019             # Conversion factor
    adc = machine.ADC(4)         # Init ADC on pin 4
    while(True):                 # Repeat forever
        x = adc.read_u16()       # Read ADC
        temp = x * K + 437.23    # Convert to celcius
        tempF= (1.8*temp) + 32 ;#Convert to Far
        R1 = round (temp,2)
        R2 = round (tempF,2)
        print(f'Temp:  {R1}°C') # Print temperature
        print(f'TempF: {R2} ºF')
        sleep_ms(1000)           # Wait for 1000ms
#end def

if __name__ == '__main__':
    main()
