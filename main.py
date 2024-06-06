# main.py -- put your code here!
import time
from machine import Pin

# Set the OUTPUT pin to on-board LED
led = Pin("LED", Pin.OUT)

# Runs forever
while True:
  led.on()
  time.sleep(0.2)
  led.off()
  time.sleep(1.0)