from machine import Pin
import time

# Use 'LED' for Pico W onboard LED, or Pin(25) for standard Pico
led = Pin("LED", Pin.OUT) 

while True:
    led.value(1)       # Turn LED on
    time.sleep(1)      # Wait 1 second
    led.value(0)       # Turn LED off
    time.sleep(1)      # Wait 1 second