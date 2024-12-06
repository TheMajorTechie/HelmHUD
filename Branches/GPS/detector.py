from time import sleep
import machine

#this code is a standalone I2C detector used for debugging.
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
devices_central = {}            #this set contains the addresses of each device connected
devices_display = {}

#I2C addresses for devices are as follows:
TEMPERATURE_ADDR = 0x10
POWER_ADDR = 0x11
HUMIDITY_ADDR = 0x12
LIGHT_ADDR = 0x29 #TSL25911FN (LIGHT)
UV_ADDR = 0x53  #LTR390-UV-1 *UV)
HEARTRATE_ADDR = 0x57 #heartrate
GAS_ADDR = 0x59 #SGP40 (VOC)
GYRO_ADDR = 0x68 #MPU9250 (9DOF)
WSTEMP_ADDR = 0x76 #(temp and humidity)
DIRECTION_ADDR = 0x14
DISPLAY_ADDR = 0x3c

devices_central = i2c_central.scan()
print("Number of devices found:")
print(len(devices_central))


for device in devices_central:
    print(hex(device))
print("Finished polling devices.")

devices_display = i2c_display.scan()
print("Number of devices found:")
print(len(devices_display))


for device in devices_display:
    print(hex(device))
print("Finished polling devices.")