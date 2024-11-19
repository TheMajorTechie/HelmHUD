import time
import machine

from machine import Pin, I2C
i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))

devices = i2c.scan()

while True:
    if(len(devices) != 0):
        print("Devices Found")
        for device in devices:
            print(device)
    else:
        print("None Found")