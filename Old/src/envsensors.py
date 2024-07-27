import machine, collections, time, asyncio

from lib.env import MPU925x as Gyroscope, BME280 as TempSensor, LTR390 as UVSensor, TSL2591 as LightSensor, SGP40 as GasSensor, VOC_Algorithm as VOC_Algorithm
from src.hr import heartrate as hr

i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))

#I2C addresses for devices are as follows:
TEMPERATURE_ADDR = 0x10
POWER_ADDR = 0x11
HUMIDITY_ADDR = 0x12
LIGHT_ADDR = 0x29 #TSL25911FN
UV_ADDR = 0x53  #LTR390-UV-1
HEARTRATE_ADDR = 0x57
#heartrate = ""
GAS_ADDR = 0x59 #SGP40
GYRO_ADDR = 0x68 #MPU9250
WSTEMP_ADDR = 0x76
DIRECTION_ADDR = 0x14

def setup():
    global devices, heartrate, temp_sensor, light_sensor, uv_sensor, gas_sensor, gyro_sensor
    devices = i2c_central.scan()
    print("Number of devices found:", len(devices))

    if len(devices) == 0:
        print("No devices found")
    else:
        for device in devices:
            if hex(device) == hex(HEARTRATE_ADDR): #detect if a device is the heartrate monitor
                heartrate = hr(i2c_central)
                print("Heart rate sensor found!")
            elif hex(device) == hex(WSTEMP_ADDR):
                temp_sensor = TempSensor.BME280(i2c_central)
                print("Temperature sensor found!")
            elif hex(device) == hex(LIGHT_ADDR):
                light_sensor = LightSensor.TSL2591(i2c_central)
                print("Light sensor found!")
            elif hex(device) == hex(UV_ADDR):
                uv_sensor = UVSensor.LTR390(i2c_central)
                print("UV sensor found!")
            elif hex(device) == hex(GAS_ADDR):
                gas_sensor = GasSensor.SGP40(i2c_central)
                print("Gas sensor found!")
            elif hex(device) == hex(GYRO_ADDR):
                gyro_sensor = Gyroscope.MPU925x(i2c_central)
                print("Gyroscope sensor found!")

    print("Finished polling devices.")