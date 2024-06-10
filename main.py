""" import dht
import machine
import time

tempSensor = dht.DHT11(machine.Pin(27))     # DHT11 Constructor 
# tempSensor = dht.DHT22(machine.Pin(27))   # DHT22 Constructor

while True:
    try:
        tempSensor.measure()
        temperature = tempSensor.temperature()
        humidity = tempSensor.humidity()
        print("Temperature is {} degrees Celsius and Humidity is {}%".format(temperature, humidity))
    except Exception as error:
        print("Exception occurred", error)
    time.sleep(2) """

from keys import DEVICE_LABEL, VARIABLE_LABEL

from boot import random_integer, sendData
from time import sleep

DELAY = 5

# Your device send a random value between 0 and 100 every five second to Ubidots
while True:
    value = random_integer(100)
    returnValue = sendData(DEVICE_LABEL, VARIABLE_LABEL, value)
    sleep(DELAY)