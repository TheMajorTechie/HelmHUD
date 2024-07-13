from time import sleep
import machine

#this code is a standalone I2C detector used for debugging.
i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
devices = {}            #this set contains the addresses of each device connected

devices = i2c_central.scan()
print("Number of devices found:")
print(len(devices))


for device in devices:
    print(hex(device))
print("Finished polling devices.")