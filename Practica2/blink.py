# ## ################################################################
# blink.py
#
# Author:  Mauricio Matamoros
# License: MIT
#
# Blinking sentinel led in the Raspberry Pi Pico using delays
#
# ## ################################################################

from machine import Pin     # Board IO Pin
from utime import sleep_ms  # Delay in milliseconds

led = Pin(25, Pin.OUT)      # Setup pin 25 (sentinel LED) as output

while(True):                # Repeat forever
   led.on()                
   sleep_ms(1)
   led.off()               
   sleep_ms(20)            # Wait for 500ms
   led.on()
