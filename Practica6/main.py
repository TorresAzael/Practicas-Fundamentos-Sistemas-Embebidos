# ## #############################################################
#
# src/pico-code-iic.py
#
# Author: Mauricio Matamoros
#
# Reads temperature from ADC using an LM35 (dummy) and sends
# it via I²C bus
#
# Pro-Tip: rename as main.py in the RP2040
# Pro-Tip: Remove anchor and main functions in i2cslave.py
#
# ## ############################################################
from i2cslave import I2CSlave
from utime import sleep_ms, sleep_us
from machine import ADC          # Board Analogic-to-Digital Converter
from utime import sleep_ms       # Delay function in milliseconds
import ustruct

#VAREF= 2.7273
VAREF = 3.3
I2C_SLAVE_ADDR = 0x0A

def main():
	setup()
	while True:
		# 1. Get temperature
		temperature = read_avg_temp(20)
		# 2. Convert temperature from pyfloat to bytes
		data = ustruct.pack('<f', temperature)

		# 3. Check if Master requested data
		if i2c.waitForRdReq(timeout=0):
			# If so, send the temperature to Master
			i2c.write(data)
		# end if

		# 3. Check if Master sent data
		if i2c.waitForData(timeout=0):
			# If so, print it
			rcv = i2c.read()
			print( rcv.decode('utf-8') )
		# end if
# end def


def read_temp():
    #Reads temperature in C from the ADC

    # The actual temperature
    vplus  = adcp.read_u16()
    # The reference temperature value, i.e. 0°C
    vminus = adcm.read_u16()
    # Calculate the difference. when V+ is smaller than V- we have negative temp
    vdiff  = vplus - vminus
    # Now, we need to convert values to the ADC resolution, AKA 2.72V/4096
    # We also know that 1°C = 0.01V so we can multiply by 2.72V / (0.01V/°C) = 272°C
    # to get °C instead of V. Analogously we can multiply VAREF by 100 but
    # since we will divide per 4096, it suffice with dividing by 40.96
    temp = vdiff * VAREF / 655.36  #40.96 version viejita
    
    return temp
# end def

def read_avg_temp(count):
    """
        Gets the average of N temperature reads
    """
    avgtemp = 0.0
    for i in range(count):
        avgtemp += read_temp()
    temp = avgtemp / count
    
    return temp

def setup():
	global i2c, adcm, adcp
	i2c = I2CSlave(address=I2C_SLAVE_ADDR)
	adcm = machine.ADC(26)         # Init ADC0
	adcp = machine.ADC(27)         # Init ADC1
# end def


if __name__ == '__main__':
	main()
