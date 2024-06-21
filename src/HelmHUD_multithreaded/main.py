import sys
sys.path.append("")

import machine
import _thread          #for multithreaded operation
import time
import struct
import bluetooth
import ssd1306
import aioble

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)

_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)	#temperature
_ENV_SENSE_POWER_UUID = bluetooth.UUID(0x2B05)	#power
_ENV_SENSE_HUMID_UUID = bluetooth.UUID(0x2A6F)	#humidity

#A set of global variables corresponding to the presence of sensors.
#There are currently three supported sensor types.
temp_present = 0
power_present = 0
humid_present = 0

screen1_row1 = 'No'
screen1_row2 = 'Devices'
screen1_row3 = 'Found'

thread0_ready = True
thread1_complete = False
thread1_exit = False

#=============================================================

class OLED_SSD1306:

    oled = ""
    oled_width = ""
    oled_height = ""

    @classmethod
    def initialize_ssd1306(self):
        #OLED setup
        self.oled_width = 128
        self.oled_height = 32
        self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, machine.I2C(0))	#default address 0x3c for ssd1306

        self.oled.text('HelmHUD', 0, 0)
        self.oled.text('Bluetooth Sensor', 0, 10)
        self.oled.text('Collator', 0, 20)

        self.oled.show()

    @classmethod
    def scroll_screen_in_out(self, screen):
        for i in range (0, (self.oled_width+1)*2, 1):
            for line in screen:
                self.oled.text(line[2], -self.oled_width+i, line[1])
                self.oled.show()
            if i!= self.oled_width:
                self.oled.fill(0)

#An object representing a Bluetooth sensor.
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

#Helper to discover sensors based on name. These sensors are in the format of HH_[sensor name] and have no protection.
#As a result, they should be considered "insecure" and are effectively garden hoses of information for anyone nearby.
async def find_sensors(sensor_name):
    print("Scanning for devices.")
    async with aioble.scan(duration_ms=10000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            if result.name() == sensor_name and _ENV_SENSE_UUID in result.services():
                print("Sensor ", sensor_name, " found: ", result.device)
                return result.device
    print("Sensor ", sensor_name, " not found.")

#=======================================================================================================

#this thread will handle user I/O and startup.
def primary_thread():
    lock.acquire()
    global shared_data_0, screen1_row1, screen1_row2, screen1_row3, thread0_ready, thread1_complete, thread1_exit
    print("Now in primary thread.")
    time.sleep(5)
    print("Printing now.")
    screen1 = [[0, 0 , screen1_row1], [0, 10, screen1_row2], [0, 20, screen1_row3]]
    OLED_SSD1306.scroll_screen_in_out(screen1)
    lock.release()
    
    secondary_thread = _thread.start_new_thread(background_thread, ())
    
    while(True):
        if(thread1_complete):
            print("Thread 1 marked as complete. Exiting thread 1.")
            thread1_exit = True
            thread1_complete = False
            time.sleep(5)
            
            secondary_thread = _thread.start_new_thread(background_thread, ())
            

#this thread will handle connections and disconnections
def background_thread():
    global shared_data_0, screen1_row1, screen1_row2, screen1_row3, thread0_ready, thread1_complete, thread1_exit
    
    thread1_complete = False
    
    print("Second thread successfully started.")
    temp_device = find_sensors("HH_Temp")
    print("Second thread phase 2")
    screen2_row2 = 'TEST'
    screen2 = [[0, 0 , screen1_row1], [0, 10, screen2_row2], [0, 20, screen1_row3]]
    
    time.sleep(5)
    lock.acquire()
    OLED_SSD1306.scroll_screen_in_out(screen2)
    lock.release()
    
    thread1_complete = True
    
    if(thread1_exit):
        print("Exiting thread 1.")
        _thread.exit()
        print("This shouldn't ever be printed!")
    
    #while True:
    #    time.sleep(10)
    #    lock.acquire()
    #    if temp_device:
    #        print("Sensor not found.")
    #    lock.release()

#a lock for inter-core synchronization
lock = _thread.allocate_lock()

OLED_SSD1306.initialize_ssd1306()
primary_thread()
