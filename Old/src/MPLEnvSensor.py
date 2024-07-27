import time
import board
from lib.MPL import adafruit_mpl3115a2

from machine import Pin, I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

# Create sensor object, communicating over the board's default I2C bus
#i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize the MPL3115A2.
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)

sensor.sealevel_pressure = 1022.5

# Reads the sensor values and print them every second.
while True:
    pressure = sensor.pressure
    print("Pressure: {0:0.3f} hectopascals".format(pressure))
    altitude = sensor.altitude
    print("Altitude: {0:0.3f} meters".format(altitude))
    temperature = sensor.temperature
    print("Temperature: {0:0.3f} Celsius".format(temperature))
    time.sleep(1.0)