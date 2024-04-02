"""import network
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('homesafenet', '@801home8567252')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
do_connect()"""

import sys
sys.path.append("")

from micropython import const

import uasyncio as asyncio
import aioble
import bluetooth

import random
import struct

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)

# org.bluetooth.characteristic.___
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)	#temperature

def setup():
    
    
    global temp_sensor
    global temp_connection
    global temp_service
    global temp_characteristic

    _ENV_SENSE_POWER_UUID = bluetooth.UUID(0x2B05)	#power
    power_sensor = None
    power_connection = None
    power_service = None
    power_characteristic = None

    _ENV_SENSE_HUMID_UUID = bluetooth.UUID(0x2A6F)	#humidity
    humid_sensor = None
    humid_connection = None
    humid_service = None
    humid_characteristic = None

async def find_sensors(sensor_name):
    print("Scanning for devices.")
    async with aioble.scan(duration_ms=10000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            if result.name() == sensor_name and _ENV_SENSE_UUID in result.services():
                print("Sensor ", sensor_name, " found: ", result.device)
                return result.device
    print("Sensor ", sensor_name, " not found.")
    return None
    
async def attempt_connection(device_type):
    """match device_type:
        case "HH_Temp":
            try:
                temp_connection = await temperature_sensor.connect()
            except asyncio.TimeoutError:
                print("Timeout during connection")
                break 
        case "HH_Power":
            try:
                power_connection = await power_sensor.connect()
            except asyncio.TimeoutError:
                print("Timeout during connection")
                break
        case "HH_Humid":
            try:
                humid_connection = await humidity_sensor.connect()
            except asyncio.TimeoutError:
                print("Timeout during connection")
                break
        case _:
            break"""
    
    print("Attempting connection.")
    try:
        temp_connection = await temp_sensor.connect()
    except asyncio.TimeoutError:
        print("Timeout during connection")
        return
    async with temp_connection:
        try:
            temp_service = await temp_connection.service(_ENV_SENSE_UUID)
            temp_characteristic = await temp_service.characteristic(_ENV_SENSE_TEMP_UUID)
        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return
    
async def main():
    setup()
    print("Starting HelmHUD.")
    temp_sensor = await find_sensors("HH_Temp")
    if not temp_sensor:
        print("No temperature sensor found.")
    else:
        print("Temperature sensor found.")
        await attempt_connection("HH_Temp")
        
    """power_sensor = await find_sensors("HH_Power")
    if not power_sensor:
        print("No power sensor found.")
        
    humidity_sensor = await find_sensors("HH_Humid")
    if not humidity_sensor:
        print("No humidity sensor found.")"""
    
asyncio.run(main())