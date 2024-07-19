import machine, collections, time, asyncio
from lib.max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM, MAX30105_PULSE_AMP_HIGH

class heartrate:

    global sensor
    global buffer
    global bpm

    def __init__(self, i2c):
        global sensor
        global buffer
        global bpm
        sensor = MAX30102(i2c)
        sensor.setup_sensor()
        sensor.set_sample_rate(400)         #400 samples are taken per second (2500 us)
        sensor.set_fifo_average(8)

        # Set LED brightness to a medium value
        sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
        sensor.shutdown()
        buffer = collections.deque((), 400)     #create a double-ended buffer with max size 400

    def __str__(self):
        return bpm * 6

    def get_raw_value(self):
        sensor.check()
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
        
    def get_readings(self):
        global buffer
        print("Reading raw values")
        sensor.wakeup()
        length_of_buffer = 400

        if len(buffer) < length_of_buffer:   #the buffer is empty and needs to be pre-filled
            for i in range(0, length_of_buffer):
                raw_value = self.get_raw_value()
                if raw_value == 0:
                    continue
                buffer.append(65536 - raw_value)
                time.sleep_us(25000)            #between each sample is 25000us (25ms)
        # #total time for a sample set: 10s (400 samples * 25ms)

        else:                   #the buffer already has data. cycle out old data and fill continuously
            for i in range(0, int(length_of_buffer / 5)):
                buffer.popleft()
                raw_value = self.get_raw_value()
                while(65536 - raw_value) > 50000:
                    raw_value = self.get_raw_value()
                buffer.append(65536 - raw_value)
                time.sleep_us(25000)

    def detect_heartbeat(self, raw_values_array):
        rise = False
        fall = False

        peaks = list()

        for i in range(1, len(raw_values_array) - 1):
            rise = (raw_values_array[i] - raw_values_array[i-1]) > 75   #detect rising edge
            fall = (raw_values_array[i + 1] - raw_values_array[i]) > 30 #detect falling edge
            if (rise == True) and (fall == True):
                rise, fall = False, False
                peaks.append(i)
        return peaks
    
    def process_values(self):
        global buffer, bpm
        sensor.shutdown()
        #subtract the smallest part of the buffer
        tempBuf = [((i - min(buffer))) * 5 for i in buffer]
        
        #detect potential heartbeats and sanitize the output to remove non-hearbeat-like structures
        peaks = self.detect_heartbeat(tempBuf)
        
        for i in range(0, len(peaks)):
            tempBuf[peaks[i]] = 65536     

        #further filter the peak detection data
        peakdetected = False
        peakcount = 0
        for i in range(1, len(tempBuf)):
            if tempBuf[i-1] == 65536:
                peakdetected = True
            if (peakdetected) and (tempBuf[i] != 65536):
                peakdetected = False
                peakcount += 1
        bpm = (peakcount * 6)
        return (bpm)
    
    async def run(self):
        global bpm
        while True:
            self.get_readings()
            bpm = self.process_values()