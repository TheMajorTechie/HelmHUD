import collections
import machine
import time
import ssd1306 as ssd1306
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import array
from machine import Timer

i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))

sensor = MAX30102(i2c_central)
sensor.setup_sensor()
sensor.set_sample_rate(400)         #400 samples are taken per second (2500 us)
sensor.set_fifo_average(8)

# Set LED brightness to a medium value
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
sensor.shutdown()
#oled_width = 128
#oled_height = 32
#oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)

global buffer
buffer = collections.deque((), 400)
prepopulated = False

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
        if (raw_values_array[i] - raw_values_array[i-1]) > 100:   #detect rising edge
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

def filter_raw_values(buffer):
    sensor.wakeup()
    
    global prepopulated
    buffer_length = 400
    #buffer = array.array('I', [0]*400)  #create an array of 400 16-bit unsigned ints

    # if prepopulated == False:
    #     print("No data populated yet. Prepopulating...")
    #     for i in range(0, 400):
    #         #print("Read")
    #         value_to_read = 65536 - get_raw_value()
    #         print(value_to_read)
    #         while(value_to_read >= 65536):
    #             print("CAUGHT ERRONEOUS READING")
    #             value_to_read = 65536 - get_raw_value()
    #         buffer.append(value_to_read)
    #         time.sleep_us(25000)            #between each sample is 25000us (25ms)
    #         #total time for a sample set: 10s (400 samples * 25ms)
    #     prepopulated = True
    #     print("Finished prepopulating")
    # else:

    while(len(buffer) < buffer_length):
        raw_value = get_raw_value()
        if(raw_value > 1000):
            value_to_read = 65536 - raw_value
    
    for i in range(0, int(buffer_length / 5)):   
        raw_value = get_raw_value()
        if(raw_value > 1000):
            value_to_read = 65536 - get_raw_value()
            buffer.append(value_to_read)
        time.sleep_us(25000)

    # for i in range(0, len(buffer)):
    #     buffer[i] = 65536 - get_raw_value()
    #     time.sleep_us(25000)            #between each sample is 25000us (25ms)
    # #total time for a sample set: 10s (400 samples * 25ms)
  
    #subtract the smallest part of the buffer
    # buffer = [((i - min(buffer))) * 5 for i in buffer]

    # print("PRE-PEAK DETECTION: ")
    # print(buffer)
    
    # #detect potential heartbeats and sanitize the output to remove non-hearbeat-like structures
    # peaks = detect_heartbeat(buffer)
    
    # for i in range(0, len(peaks)):
    #     buffer[peaks[i]] = 65536

    # # duplicate_count = 0

    # # #loop through the buffer
    # # for i in range(0, len(buffer)):
    # #     if buffer[i] == 65536:
    # #         j = i
    # #         while(buffer[j] == 65536):
    # #             duplicate_count += 1
    # #             j += 1
    # #         if duplicate_count > 5:
    # #             buffer[i] = 0

    
    
    # # for i in range(0, len(detect_heartbreat(buffer))):
    # #     buffer[i] = 65536
    # #     #print(i)
    # #     continue
    # print("POST PEAK DETECTION: ")
    # print(buffer)

    # print("\n\n\n")
    # sensor.shutdown()

    # #further filter the peak detection data
    # peakdetected = False
    # peakcount = 0
    # for i in range(1, len(buffer)):
    #     if buffer[i-1] == 65536:
    #         peakdetected = True
    #     if (peakdetected) and (buffer[i] != 65536):
    #         peakdetected = False
    #         peakcount += 1

    # print("Peaks in 10s: ", peakcount)
    # print("BPM: ", peakcount * 6)
    # print("\n\n\n")

def GetRawValues(buffer): 
    sensor.wakeup()
    buffer_length = 400

    #read in values to initially populate the buffer. we won't be worrying much about these in the long run
    # while(len(buffer) < buffer_length):
    #     print("Prepopulating buffer")
    #     raw_value = get_raw_value()
    #     while(raw_value > 1000):
    #         value_to_read = 65536 - raw_value
    #     buffer.append(value_to_read)

    # raw_value = get_raw_value()
    # while(raw_value > 1000):
    #     print("ERROR CAUGHT")
    #     value_to_read = 65536 - get_raw_value()
    # buffer.append(value_to_read)
    # time.sleep_us(25000)

    raw_value = get_raw_value()
    print(raw_value)

    # #now continuously read in values
    # for i in range(0, int(buffer_length / 5)):   
    #     raw_value = get_raw_value()
    #     if(raw_value > 1000):
    #         value_to_read = 65536 - get_raw_value()
    #         buffer.append(value_to_read)
    #     time.sleep_us(25000)

def CalculateBPM_handler(timer):
    global buffer
    print(buffer)
    sensor.shutdown()

    #subtract the smallest part of the buffer
    buffer = [((i - min(buffer))) * 5 for i in buffer]

    print("PRE-PEAK DETECTION: ")
    print(buffer)
    
    #detect potential heartbeats and sanitize the output to remove non-hearbeat-like structures
    peaks = detect_heartbreat(buffer)
    
    for i in range(0, len(peaks)):
        buffer[peaks[i]] = 65536

    print("POST PEAK DETECTION: ")
    print(buffer)

    print("\n\n\n")

    

while True:
    #print(get_raw_value())
    #time.sleep_us(25000)
    filter_raw_values()