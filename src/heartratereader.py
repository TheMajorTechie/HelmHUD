import collections
import machine
import time
#import lib.ssd1306 as ssd1306
from lib.max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM, MAX30105_PULSE_AMP_HIGH
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

buffer = collections.deque((), 400)

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
    else:
        return 0        #consider throwing an exception or doing some kind of intelligent error handling instead 
    
def detect_heartbeat(raw_values_array):
    rise = False
    fall = False

    peaks = list()

    for i in range(1, len(raw_values_array) - 1):
        if (raw_values_array[i] - raw_values_array[i-1]) > 25:   #detect rising edge
            rise = True
            #print("RISE: ", i)
        if (raw_values_array[i + 1] - raw_values_array[i]) > 10: #detect falling edge
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

def get_raw_values(buffer):
    sensor.wakeup()
    length_of_buffer = 400

    if len(buffer) < length_of_buffer:   #the buffer is empty and needs to be pre-filled
        for i in range(0, length_of_buffer):
            raw_value = get_raw_value()
            while(65536 - raw_value) > 50000:
                raw_value = get_raw_value()
                #print(65536-raw_value)
            buffer.append(65536 - raw_value)
            time.sleep_us(25000)            #between each sample is 25000us (25ms)
    # #total time for a sample set: 10s (400 samples * 25ms)

    else:                   #the buffer already has data. cycle out old data and fill continuously
         for i in range(0, int(length_of_buffer / 5)):
            buffer.popleft()
            raw_value = get_raw_value()
            while(65536 - raw_value) > 50000:
                raw_value = get_raw_value()
            buffer.append(65536 - raw_value)
            time.sleep_us(25000)

def process_values(timer):
    global buffer
    sensor.shutdown()
    #subtract the smallest part of the buffer
    tempBuf = [((i - min(buffer))) * 5 for i in buffer]

    print("PRE-PEAK DETECTION: ")
    print(tempBuf)
    
    #detect potential heartbeats and sanitize the output to remove non-hearbeat-like structures
    peaks = detect_heartbeat(tempBuf)
    
    for i in range(0, len(peaks)):
        tempBuf[peaks[i]] = 65536

    print("POST PEAK DETECTION: ")
    print(tempBuf)

    print("\n\n\n")
    

    #further filter the peak detection data
    peakdetected = False
    peakcount = 0
    for i in range(1, len(tempBuf)):
        if tempBuf[i-1] == 65536:
            peakdetected = True
        if (peakdetected) and (tempBuf[i] != 65536):
            peakdetected = False
            peakcount += 1

    print("Peaks in 10s: ", peakcount)
    print("BPM: ", peakcount * 6)
    print("\n\n\n")

def filter_raw_values():
    global buffer
    # sensor.wakeup()

    # buffer = array.array('I', [0]*400)  #create an array of 400 16-bit unsigned ints
    # for i in range(0, 25):
    #         buffer[0] = get_raw_value()

    # for i in range(0, len(buffer)):
    #     buffer[i] = 65536 - get_raw_value()
    #     time.sleep_us(25000)            #between each sample is 25000us (25ms)
    # #total time for a sample set: 10s (400 samples * 25ms)

    get_raw_values(buffer)
  
    #subtract the smallest part of the buffer
    tempBuf = [((i - min(buffer))) * 5 for i in buffer]

    print("PRE-PEAK DETECTION: ")
    print(tempBuf)
    
    #detect potential heartbeats and sanitize the output to remove non-hearbeat-like structures
    peaks = detect_heartbeat(tempBuf)
    
    for i in range(0, len(peaks)):
        tempBuf[peaks[i]] = 65536

    print("POST PEAK DETECTION: ")
    print(tempBuf)

    print("\n\n\n")
    sensor.shutdown()

    #further filter the peak detection data
    peakdetected = False
    peakcount = 0
    for i in range(1, len(tempBuf)):
        if tempBuf[i-1] == 65536:
            peakdetected = True
        if (peakdetected) and (tempBuf[i] != 65536):
            peakdetected = False
            peakcount += 1

    print("Peaks in 10s: ", peakcount)
    print("BPM: ", peakcount * 6)
    print("\n\n\n")

if __name__ == "__main__":
    soft_timer = Timer(mode=Timer.PERIODIC, period=15000, callback=process_values)

    while True:
        #print(get_raw_value())
        #time.sleep_us(25000)
        #filter_raw_values()
        #time.sleep(1)
        print("RUNNING GET VALUES")
        get_raw_values(buffer)