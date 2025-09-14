
# ## ################################################################
# blink-timer.py
#
# Author:  Torres Azael 
# License: MIT
#
# Blinking sentinel led in the Raspberry Pi Pico using PWM
#
# ## ################################################################

from machine import Pin,PWM # Board IO Pin and PWM
from machine import Timer   # Hardware timer

def blink(timer):           # Callback function
    led.toggle()            # Toggle the led
#end def

timer = Timer()             # Create the Timer object
timer.init(freq=50,        # Timer frequency set to 2.5Hz
    mode=Timer.PERIODIC,    # Timer will run endlessly (not one-shot)
    callback=blink          # Set callback function: blink
)

led = Pin(25, Pin.OUT)      # Setup pin 25 (sentinel LED) as output

timer = Timer()             # Create the Timer object
timer.init(freq=50,        # Timer frequency set to 2.5Hz
    mode=Timer.PERIODIC,    # Timer will run endlessly (not one-shot)
    callback=blink          # Set callback function: blink
)
