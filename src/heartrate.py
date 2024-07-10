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
sensor.set_sample_rate(400)         #400 samples are taken per second.
sensor.set_fifo_average(8)
# Set LED brightness to a medium value
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)

# def read_heart_rate():
#     ir_buffer = array.array('I', [0]*100)  # Buffer to store IR values
#     while True:
#         sensor.check()
#         if sensor.available():
#             red, ir = sensor.pop_red_from_storage(), sensor.pop_ir_from_storage()
#             ir_buffer.append(ir)
#             ir_buffer.pop(0)
#             heart_rate = calculate_heart_rate(ir_buffer)  # Calculate heart rate from the buffer
#             if heart_rate:
#                 yield heart_rate

def read_heart_rate():
    ir_buffer = array.array('I', [0]*100)  # Buffer to store IR values
    buffer_index = 0
    while True:
        sensor.check()
        if sensor.available():
            red, ir = sensor.pop_red_from_storage(), sensor.pop_ir_from_storage()
            ir_buffer[buffer_index] = ir
            buffer_index = (buffer_index + 1) % 100
            heart_rate = calculate_heart_rate(ir_buffer)  # Calculate heart rate from the buffer
            if heart_rate:
                yield heart_rate

def calculate_heart_rate(ir_values):
    # Simple peak detection algorithm
    peaks = detect_peaks(ir_values)
    if len(peaks) >= 2:
        peak_intervals = [peaks[i] - peaks[i-1] for i in range(1, len(peaks))]
        avg_peak_interval = sum(peak_intervals) / len(peak_intervals)
        heart_rate = 60 / (avg_peak_interval * 0.02)  # Convert to BPM (assuming 20ms interval between samples)
        return int(heart_rate)
    return None

def detect_peaks(data):
    threshold = max(data) * 0.6  # 60% of the max value
    return [i for i in range(1, len(data) - 1) if data[i-1] < data[i] > data[i+1] and data[i] > threshold]

def display_heart_rate(oled, heart_rate):
    oled.fill(0)  # Clear the screen
    oled.text("Heart Rate:", 0, 0)
    oled.text(f"{heart_rate} BPM", 0, 10)
    oled.show()

def main():
    hr_gen = read_heart_rate()

    while True:
        try:
            heart_rate = next(hr_gen)
            print("Heart Rate:", heart_rate)
            display_heart_rate(oled, heart_rate)
        except StopIteration:
            break
        time.sleep(1)

if __name__ == "__main__":
    main()