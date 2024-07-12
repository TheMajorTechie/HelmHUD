import machine
import time
import lib.ssd1306 as ssd1306

# Set up ADC pin (GP26 is ADC0)
adc = machine.ADC(machine.Pin(26))

# Set up I2C for OLED
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))

# Initialize OLED display
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)

# Function to read and convert the ADC value to voltage
def read_voltage():
    # Read raw ADC value (0-65535)
    raw_value = adc.read_u16()
    # Convert raw value to voltage (0-3.3V)
    voltage = raw_value * (3.3 / 65535)
    return voltage

# Function to estimate battery life based on voltage
def estimate_battery_life(voltage):
    # Example thresholds for battery life estimation
    if voltage > 3.2:
        return "Full"
    elif voltage > 3.0:
        return "Medium"
    else:
        return "Critical"

# Function to display voltage and battery status on OLED
def display_battery_status(oled, voltage, status):
    oled.fill(0)  # Clear the screen
    oled.text(f"Voltage: {voltage:.2f}V", 0, 0)
    oled.text(f"Status: {status}", 0, 10)
    oled.show()

while True:
    voltage = read_voltage()
    battery_status = estimate_battery_life(voltage)
    display_battery_status(oled, voltage, battery_status)
    time.sleep(1)