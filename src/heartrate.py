import machine
import time
import ssd1306
from MAX30102 import MAX30102
import array
import math

# Initialize I2C for MAX30102 and OLED
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))
sensor = MAX30102(i2c)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def read_heart_rate():
    ir_buffer = array.array('I', [0]*100)  # Buffer to store IR values
    while True:
        red, ir = sensor.read_sequential()  # Read data from the sensor
        ir_buffer.append(ir)
        ir_buffer.pop(0)
        heart_rate = calculate_heart_rate(ir_buffer)  # Calculate heart rate from the buffer
        if heart_rate:
            yield heart_rate

def calculate_heart_rate(ir_values):
    # Simple peak detection algorithm
    peaks = detect_peaks(ir_values)
    if len(peaks) >= 2:
        peak_intervals = []
        for i in range(1, len(peaks)):
            peak_intervals.append(peaks[i] - peaks[i-1])
        avg_peak_interval = sum(peak_intervals) / len(peak_intervals)
        heart_rate = 60 / (avg_peak_interval * 0.02)  # Convert to BPM (assuming 20ms interval between samples)
        return int(heart_rate)
    return None

def detect_peaks(data):
    threshold = max(data) * 0.6  # 60% of the max value
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i-1] < data[i] > data[i+1] and data[i] > threshold:
            peaks.append(i)
    return peaks

def display_heart_rate(oled, heart_rate):
    oled.fill(0)  # Clear the screen
    oled.text("Heart Rate:", 0, 0)
    oled.text(str(heart_rate) + " BPM", 0, 10)
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
