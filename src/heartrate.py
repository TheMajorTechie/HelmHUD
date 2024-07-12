import collections
import machine
import time
import lib.ssd1306 as ssd1306
from lib.max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM, MAX30105_PULSE_AMP_HIGH
import array

i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))

sensor = MAX30102(i2c_central)
sensor.setup_sensor()
sensor.set_sample_rate(400)         #400 samples are taken per second (2500 us)
sensor.set_fifo_average(8)

# Set LED brightness to a medium value
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
sensor.shutdown()
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)

def get_raw_value():
    sensor.check()
    if sensor.available():
        # Access the storage FIFO and gather the readings (integers)
        ir_reading = sensor.pop_ir_from_storage()
               
        #if the reading is 0, try reading it again until it isn't
        while ir_reading == 0:
            sensor.check()
            ir_reading = sensor.pop_ir_from_storage()
        return ir_reading
    return 0
    
def detect_heartbeat(raw_values_array):
    rise = False
    fall = False

    peaks = list()

    for i in range(1, len(raw_values_array) - 1):
        if (raw_values_array[i] - raw_values_array[i-1]) > 100:   #detect rising edge
            rise = True
        if (raw_values_array[i + 1] - raw_values_array[i]) > 10: #detect falling edge
            fall = True
        if (rise == True) and (fall == True):
            #print("PEAK AT: ", i)
            rise, fall = False, False
            peaks.append(i)

    return peaks

def filter_raw_values():
    sensor.wakeup()

    bufferlength = 400
    buffer = array.array('I', [0]*bufferlength)  #create an array of 400 16-bit unsigned ints
    for i in range(0, 25):
            buffer[0] = get_raw_value()

    for i in range(0, bufferlength):
        buffer[i] = 65536 - get_raw_value()
        time.sleep_us(25000)            #between each sample is 25000us (25ms)
    #total time for a sample set: 10s (400 samples * 25ms)
  
    #subtract the smallest part of the buffer
    buffer = [((i - min(buffer))) * 5 for i in buffer]

    print("PRE-PEAK DETECTION: ")
    print(buffer)
    
    #detect potential heartbeats and sanitize the output to remove non-hearbeat-like structures
    peaks = detect_heartbeat(buffer)
    
    for peak in peaks:
        buffer[peak] = 65536

    print("POST PEAK DETECTION: ")
    print(buffer)
    print("\n\n\n")
    
    sensor.shutdown()

    #further filter the peak detection data
    peakdetected = False
    peakcount = 0
    for i in range(1, len(buffer)):
        if buffer[i-1] == 65536:
            peakdetected = True
        if (peakdetected) and (buffer[i] != 65536):
            peakdetected = False
            peakcount += 1

    print("Peaks in 10s: ", peakcount)
    print("BPM: ", peakcount * 6)
    print("\n\n\n")
    display_heart_rate(oled, peakcount*6)

def display_heart_rate(oled, heart_rate):
    oled.fill(0)  # Clear the screen
    oled.text(f"{heart_rate} BPM", 0, 10)
    oled.show()

while True:
    filter_raw_values()
    time.sleep(1)
