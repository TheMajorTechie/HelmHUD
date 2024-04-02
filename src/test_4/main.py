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
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
_ENV_SENSE_POWER_UUID = bluetooth.UUID(0x2B05)	#power
_ENV_SENSE_HUMID_UUID = bluetooth.UUID(0x2A6F)	#humidity

temp_present = 0
power_present = 0
humid_present = 0

class Sensor:
    def __init__(self, device):
        self.device = device
        
    def set_connection(self, connection):
        self.connection = connection
        
    def set_service(self, service):
        self.service = service
        
    def set_characteristic(self, characteristic):
        self.characteristic = characteristic

# Helper to decode the temperature characteristic encoding (sint16, hundredths of a degree).
def _decode_temperature(data):
    return struct.unpack("<h", data)[0] / 100

async def find_sensors(sensor_name):
    print("Scanning for devices.")
    async with aioble.scan(duration_ms=10000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            if result.name() == sensor_name and _ENV_SENSE_UUID in result.services():
                print("Sensor ", sensor_name, " found: ", result.device)
                return result.device
    print("Sensor ", sensor_name, " not found.")
    return None

async def main():
    #Set up Bluetooth temperature sensor
    temp_device = await find_sensors("HH_Temp")
    if not temp_device:
        print("Temperature sensor not found")
    else:
        temp_sensor = Sensor(temp_device)
        global temp_present
        temp_present = 1
    try:
        print("Connecting to", temp_sensor.device)
        temp_sensor.set_connection(await temp_sensor.device.connect())
    except asyncio.TimeoutError:
        print("Timeout during connection")
        global temp_present
        temp_present = 0

    async with temp_sensor.connection:
        try:
            temp_sensor.set_service(await temp_sensor.connection.service(_ENV_SENSE_UUID))
            temp_characteristic = await temp_sensor.service.characteristic(_ENV_SENSE_TEMP_UUID)
        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return

        while True:
            temp_deg_c = _decode_temperature(await temp_characteristic.read())
            print("Temperature: {:.2f}".format(temp_deg_c))
            await asyncio.sleep_ms(1000)
    

asyncio.run(main())

"""import machine
import bluetooth
import utime
import ssd1306
from ble_simple_peripheral import BLESimplePeripheral

#the LED is on the specialty 'LED' pin for the pico w
led = machine.Pin('LED', machine.Pin.OUT)
led_state = 0

adc = machine.ADC(4)

ble = bluetooth.BLE()

simplePeriph = BLESimplePeripheral(ble)

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, machine.I2C(0))	#default address 0x3c for ssd1306

oled.text('Hello, World 1!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)
screen1_row1 = 'row1'
screen1_row2 = 'row2'
screen1_row3 = 'row3'

oled.show()

led.value(0)

#A callback for the simple bluetooth peripheral that we call on receiving data
def on_SPCbRx(data):
    decoded_data = data.decode("utf-8")[:len(data)-2]
    print("Data received: ", data)
    global led_state
    if data == b'toggle\r\n':
        led.value(not led_state)
        led_state = 1 - led_state
    else:
        print("Non LED command. Printing to OLED and BT console.")
        #show_text(decoded_data, 0, 10)
        global screen1_row1
        screen1_row1 = decoded_data

#the weakness of this current method is that text gets overwritten when trying to
#display both temperature and BT data at once!
def show_text(text, position_x, position_y):
    oled.fill(0)
    for char in text:		# show text character by character for a neat effect
        utime.sleep(0.250)
        simplePeriph.send(str(char))
        oled.text(str(char), position_x, position_y)
        position_x += 8
        oled.show()
    simplePeriph.send('\r\n')
    
def scroll_screen_in_out(screen):
  for i in range (0, (oled_width+1)*2, 1):
    for line in screen:
      oled.text(line[2], -oled_width+i, line[1])
    oled.show()
    if i!= oled_width:
      oled.fill(0)
        
def refresh_temp_display(temp_c, temp_f):
    tempdisp = "Temps: {}C, {}F".format(temp_c,temp_f)
    #show_text(tempdisp, 0, 0)
    global screen1_row2
    screen1_row2 = tempdisp
    utime.sleep_ms(500)

screen1 = [[0, 0 , screen1_row1], [0, 10, screen1_row2], [0, 20, screen1_row3]]
scroll_screen_in_out(screen1)

while True:
    if simplePeriph.is_connected():
        simplePeriph.on_write(on_SPCbRx)
    ADC_v = adc.read_u16() * (3.3/65536)
    temp_c = 27 - (ADC_v - 0.706)/0.001721
    temp_f = 32 + (1.8*temp_c)
    refresh_temp_display(str(temp_c)[:4], str(temp_f)[:4])
    screen1 = [[0, 0 , screen1_row1], [0, 10, screen1_row2], [0, 20, screen1_row3]]
    scroll_screen_in_out(screen1)
    
        
        
"""

