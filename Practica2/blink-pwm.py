## ################################################################
# blink_pwm.py
#
# Author:  Torres Anguiano Azael Arturo
# License: MIT
#
# Blinking sentinel led in the Raspberry Pi Pico using timers
#
# ## ################################################################

from machine import Pin,PWM     # Board IO Pin and PWM

led = Pin(25, Pin.OUT)      # Setup pin 25 (sentinel LED) as output
pwm = PWM(led)              # Assignment of PWM to Led
pwm.duty_u16(400)           # Definition of duty cyclo, 16 bits, as an unsigned 16-bits value between 0 to 65545