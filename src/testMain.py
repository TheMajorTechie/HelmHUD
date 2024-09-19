import collections
from time import sleep
from machine import Pin, I2C
import _thread
from lib.max30102 import MAX30102
import array
import math
import time
from src.hr import heartrate as hr
from src.pollenvsense import TempSensor, LightSensor, UVSensor, GasSensor, Gyroscope, MPLSensor
#from src.MPLEnvSensor import envSensor as temp_sensor
import asyncio

#==========================================================

global_path = 0         #functions that write to global_path need to use 
                        #"global global_path" in their setup. reading does not need to do this.

device_id = 0           #the device ID for the central pi pico is and will always be 0.
device_polling = 0      #the device ID for the current device being polled.

# I2C addresses for devices are as follows:
TEMPERATURE_ADDR = 0x10
POWER_ADDR = 0x11
HUMIDITY_ADDR = 0x12
LIGHT_ADDR = 0x29  # TSL25911FN
UV_ADDR = 0x53    # LTR390-UV-1
HEARTRATE_ADDR = 0x57
WSTEMP_ADDR = 0x76

# Set up I2C for sensor peripherals on the I2C1 bus
#Hearteat Sensor
i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
#MPL Sensor
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
#Button
button = machine.Pin(15, Pin.IN, Pin.PULL_DOWN) 

devices = {}  # This set contains the addresses of each device connected

#============================================UTILITY FUNCTIONS==========================

# Initialize sensors
heartrate = None
temp_sensor = None

#Count of times the button has been pressed
buttonPresses = 0
#Last time we pressed the button
lastPress = 0

# Scan for I2C devices
def setup():
    global devices, heartrate, temp_sensor
    devices = i2c_central.scan()
    print("Number of devices found:", len(devices))

    for device in devices:
        if device == HEARTRATE_ADDR:  # Detect if a device is the heart rate monitor
            heartrate = hr(i2c_central)
            print("Heart rate sensor found!")
        elif device == WSTEMP_ADDR:
            temp_sensor = TempSensor(i2c_central)
            print("Temperature sensor found!")

    sleep(2)
    print("Finished polling devices.")

# Poll sensors
async def poll_sensors():
    print("Pretend this is some very neato data lol")
    if heartrate:
        print(heartrate.process_values())
    elif temp_sensor:
        print(temp_sensor.process_values())
        
# Main method running on core 1.
def core1_main():
    global lock
    print("Core 1 main function")
    lock.acquire()
    setup()
    lock.release()
    await poll_sensors()
    _thread.exit()
    
    print("Please wait 5s for HelmHUD to begin operation.")
    lock = _thread.allocate_lock()
    sleep(5)
    print("Starting.")

# core0_main()

async def main():
    lastPress = 0
    while True:
        if buttonPresses != lastPress:
            runSetup()
            lastPress = buttonPresses

def buttonPressed(pin):
    global buttonPresses, lastPress
    countTime = time.ticks_ms()
    if (countTime - lastPress) > 200: 
        buttonPresses += 1
        lastPress = countTime

button.irq(trigger=machine.Pin.IRQ_FALLING, handler = buttonPressed)


def runSetup():
    print("Setting up")
    setup()
    if heartrate:
        heartrate.get_readings()
        print(heartrate.process_values())
    elif temp_sensor:
        temp_sensor.get_reading()
        print(temp_sensor.process_values())
      
      
loop = asyncio.get_event_loop()
loop.run_until_complete(main())