import time

from lib.micropython_mpl3115a2 import mpl3115a2

from machine import Pin, I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

sensor = mpl3115a2.MPL3115A2(i2c)

# Reads the sensor values and print them every second.
while True:
    pressure = sensor.pressure
    print("Pressure: {0:0.3f} hectopascals".format(pressure))
    altitude = sensor.altitude
    print("Altitude: {0:0.3f} meters".format(altitude))
    temperature = sensor.temperature
    print("Temperature: {0:0.3f} Celsius".format(temperature))
    time.sleep(1.0)