import collections
from time import sleep
import machine
import _thread
import lib.ssd1306 as ssd1306
from lib.max30102 import MAX30102
import array
import math
from src.hr import heartrate as hr
import asyncio

#==========================================================

global_path = 0         #functions that write to global_path need to use 
                        #"global global_path" in their setup. reading does not need to do this.

device_id = 0           #the device ID for the central pi pico is and will always be 0.
device_polling = 0      #the device ID for the current device being polled.

#I2C addresses for devices are as follows:
TEMPERATURE_ADDR = 0x10
POWER_ADDR = 0x11
HUMIDITY_ADDR = 0x12
HEARTRATE_ADDR = 0x57
#heartrate = ""
DIRECTION_ADDR = 0x14

#set up I2C for sensor peripherals on the I2C1 bus. The display is located on I2C0.
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
devices = {}            #this set contains the addresses of each device connected

#set up OLED display
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)
oled.text('HelmHUD', 0, 0)
oled.text('Sensor', 0, 10)
oled.text('Collator', 0, 20)
oled.show()

#a basic default "screen" to display.
screen1_row1 = 'No'
screen1_row2 = 'Devices'
screen1_row3 = 'Found'
screen1 = [[0,0, screen1_row1], [0,10, screen1_row2], [0,20, screen1_row3]]

#============================================UTILITY FUNCTIONS==========================

#scan for I2C devices
def setup():
    global devices      #this is used to hold the devices listed.

    #global variables to "store" the devices
    global heartrate                        
    devices = i2c_central.scan()
    oled.text('Devices found:', 0, 0)
    oled.text(str(len(devices)), 0, 20)
    print("Number of devices found:")
    print(len(devices))
    
    if len(devices) == 0:
        scroll_display(screen1)
    
    else:
        for device in devices:
            if hex(device) == hex(HEARTRATE_ADDR):           #detect if a device is the heartrate monitor
                heartrate = hr(i2c_central)
                print("Heart rate sensor found!")

            oled.text('', 0, 10)
            oled.text(hex(device), 0, 10)
            oled.show()
            sleep(2)
    print("Finished polling devices.")

#now poll the devices that were scanned. This function will eventually be used for grabbing data from sensors.
async def poll_sensors():
    print("Pretend this is some very neato data lol")
    print(heartrate.process_values())

#a helper function for scrolling text on the SSD1306 screen.
def scroll_display(screen):
    for i in range (0, (oled_width + 1)*2, 1):
        for line in screen:
            oled.text(line[2], -oled_width+i, line[1])
        oled.show()
        if i != oled_width:
            oled.fill(0)

#===============================================MAIN CORE FUNCTIONS=============================

#the main method running on core 0.
#TODO: HAVE CORE 0 "WAKE UP" CORE 1 ON A TIMER
def core0_main():
    global lock
    print("Core 0 main function")
    screen2_row1 = ''
    screen2_row2 = 'Scanning for devices...'
    screen2_row3 = ''
    screen2 = [[0,0, screen2_row1], [0,10, screen2_row2], [0,20, screen2_row3]]
    lock.acquire()
    scroll_display(screen2)
    lock.release()
    print("Starting second thread")
    second_thread = _thread.start_new_thread(core1_main, ())
    sleep(5)

#the main method running on core 1.
async def core1_main():
    global lock
    print("Core 1 main function")
    lock.acquire()
    setup()
    lock.release()
    await poll_sensors()
    _thread.exit()
        
#===========================================================

print("Please wait 5s for HelmHUD to begin operation.")
lock = _thread.allocate_lock()
sleep(5)
print("Starting.")

#core0_main()

async def main():
    print("Setting up")
    setup()
    heartrate.get_readings()
    print(heartrate.process_values())
    


loop = asyncio.get_event_loop()
loop.run_until_complete(main())