import collections
import machine
import time
import ssd1306 as ssd1306
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import array

i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))

sensor = MAX30102(i2c_central)
sensor.setup_sensor()
sensor.set_sample_rate(400)         #400 samples are taken per second (2500 us)
sensor.set_fifo_average(8)

# Set LED brightness to a medium value
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)

def get_raw_value():
    sensor.check()
    # if sensor.available():
    #     return int(sensor.pop_ir_from_storage())
    if sensor.available():
        # Access the storage FIFO and gather the readings (integers)
        ir_reading = sensor.pop_ir_from_storage()
               
        #if the reading is 0, try reading it again until it isn't
        if ir_reading == 0:
            while(True):
                sensor.check()
                ir_reading = sensor.pop_ir_from_storage()
                if(ir_reading != 0):
                    break
        return ir_reading
    
def detect_heartbreat(raw_values_array):
    rise = False
    fall = False

    peaks = list()

    for i in range(1, len(raw_values_array) - 1):
        if (raw_values_array[i] - raw_values_array[i-1]) > 10:   #detect rising edge
            rise = True
            #print("RISE: ", i)
        if (raw_values_array[i + 1] - raw_values_array[i] > 10): #detect falling edge
            fall = True
            #print("FALL: ", i)
        # if (raw_values_array[i] == raw_values_array[i-1]) or (raw_values_array[i] == raw_values_array[i+1]):
        #     continue
        if (rise == True) and (fall == True):
            #print("PEAK AT: ", i)
            rise, fall = False, False
            peaks.append(i)
    #print(peaks)

    return peaks

def find_peaks(raw_values_array, threshold):
    #pick out peaks within the range of ir values where there is both a localized peak 
    #(surrounding values are lower) and it surpasses the theshold
    
    peaks = []
    for i in range(1, len(raw_values_array) - 1):
        if (raw_values_array[i-1] < raw_values_array[i] >raw_values_array[i+1] and raw_values_array[i] > threshold):
            print("PEAK")
    
    return [i for i in range(1, len(raw_values_array) - 1) 
            if raw_values_array[i-1] < raw_values_array[i] > raw_values_array[i+1] and raw_values_array[i] > threshold]

def filter_raw_values():
    buffer = array.array('I', [0]*400)  #create an array of 400 16-bit unsigned ints
    for i in range(0, len(buffer)):
        buffer[i] = get_raw_value()
        time.sleep_us(25000)            #between each sample is 25000us (25ms)
    #total time for a sample set: 10s (400 samples * 25ms)
  
    #subtract the smallest part of the buffer
    buffer = [((i - min(buffer))) * 5 for i in buffer]

    print("PRE-PEAK DETECTION: ")
    print(buffer)
    
    #detect potential heartbeats and sanitize the output to remove non-hearbeat-like structures
    peaks = detect_heartbreat(buffer)
    
    for i in range(0, len(peaks)):
        buffer[peaks[i]] = 65536

    # duplicate_count = 0

    # #loop through the buffer
    # for i in range(0, len(buffer)):
    #     if buffer[i] == 65536:
    #         j = i
    #         while(buffer[j] == 65536):
    #             duplicate_count += 1
    #             j += 1
    #         if duplicate_count > 5:
    #             buffer[i] = 0

    
    
    # for i in range(0, len(detect_heartbreat(buffer))):
    #     buffer[i] = 65536
    #     #print(i)
    #     continue
    print("POST PEAK DETECTION: ")
    print(buffer)

    print("\n\n\n")

    

while True:
    #print(get_raw_value())
    #time.sleep_us(25000)
    filter_raw_values()