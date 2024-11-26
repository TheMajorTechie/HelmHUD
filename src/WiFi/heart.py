import collections
import machine
import time
import network  # Import network module for Wi-Fi
import socket   # Import socket module for networking
from lib.max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import array
from machine import Timer
import asyncio

# --- Network Setup ---
# Define the SSID of the Access Point to connect to
AP_SSID = 'PicoAP4'

# Server IP and Port
SERVER_IP = '192.168.4.1'  # Replace with the actual IP if different
SERVER_PORT = 8080

# Initialize the Station interface
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Scan for available networks
networks = sta.scan()
print('Available networks:')
for net in networks:
    ssid = net[0].decode()
    print(ssid)

# Check if 'PicoAP4' is in the list
if AP_SSID not in [net[0].decode() for net in networks]:
    print(f"Access Point '{AP_SSID}' not found. Check if the AP is active and nearby.")
else:
    print(f"Access Point '{AP_SSID}' found. Attempting to connect...")
    sta.connect(AP_SSID)

    # Wait for connection
    while not sta.isconnected():
        print('Connecting to network...')
        time.sleep(1)

print('Station Connected')
print('Network config:', sta.ifconfig())

# Initialize I2C for the sensor
i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))

sensor = MAX30102(i2c_central)
sensor.setup_sensor()
sensor.set_sample_rate(400)         # 400 samples are taken per second (2500 us)
sensor.set_fifo_average(8)

# Set LED brightness to a medium value
sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
sensor.shutdown()

buffer = collections.deque((), 400)

def setup_sensor():
    global sensor
    global i2c_central
    global buffer

    i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))

    sensor = MAX30102(i2c_central)
    sensor.setup_sensor()
    sensor.set_sample_rate(400)         # 400 samples are taken per second (2500 us)
    sensor.set_fifo_average(8)

    # Set LED brightness to a medium value
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
    sensor.shutdown()

    buffer = collections.deque((), 400)

def get_raw_value():
    sensor.check()
    if sensor.available():
        ir_reading = sensor.pop_ir_from_storage()
        # If the reading is 0, try reading it again until it isn't
        if ir_reading == 0:
            while True:
                sensor.check()
                ir_reading = sensor.pop_ir_from_storage()
                if ir_reading != 0:
                    break
        return ir_reading
    else:
        return 0  # Consider throwing an exception or handling errors intelligently

def detect_heartbeat(raw_values_array):
    rise = False
    fall = False
    peaks = []

    for i in range(1, len(raw_values_array) - 1):
        if (raw_values_array[i] - raw_values_array[i - 1]) > 75:  # Detect rising edge
            rise = True
        if (raw_values_array[i + 1] - raw_values_array[i]) > 30:  # Detect falling edge
            fall = True
        if rise and fall:
            rise, fall = False, False
            peaks.append(i)
    return peaks

def get_raw_values():
    global buffer
    print("Reading raw values")
    sensor.wakeup()
    length_of_buffer = 400

    if len(buffer) < length_of_buffer:   # The buffer is empty and needs to be pre-filled
        for i in range(length_of_buffer):
            raw_value = get_raw_value()
            if raw_value == 0:
                continue
            buffer.append(65536 - raw_value)
            time.sleep_us(25000)  # Between each sample is 25000us (25ms)
    else:  # The buffer already has data. Cycle out old data and fill continuously
        for i in range(int(length_of_buffer / 5)):
            buffer.popleft()
            raw_value = get_raw_value()
            while (65536 - raw_value) > 50000:
                raw_value = get_raw_value()
            buffer.append(65536 - raw_value)
            time.sleep_us(25000)

def process_values():
    global buffer
    sensor.shutdown()
    # Subtract the smallest value in the buffer and scale
    tempBuf = [((i - min(buffer))) * 5 for i in buffer]

    print("PRE-PEAK DETECTION: ")
    print(tempBuf)

    # Detect potential heartbeats
    peaks = detect_heartbeat(tempBuf)

    for peak in peaks:
        tempBuf[peak] = 65536

    print("POST PEAK DETECTION: ")
    print(tempBuf)
    print("\n\n\n")

    # Count the number of peaks
    peak_detected = False
    peak_count = 0
    for i in range(1, len(tempBuf)):
        if tempBuf[i - 1] == 65536:
            peak_detected = True
        if peak_detected and tempBuf[i] != 65536:
            peak_detected = False
            peak_count += 1

    bpm = peak_count * 6  # Since we collect data over 10 seconds
    print("Peaks in 10s: ", peak_count)
    print("BPM: ", bpm)
    print("\n\n\n")

    # --- Send BPM data to server ---
    try:
        # Create a socket and connect to the server
        client_socket = socket.socket()
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Send BPM data to the server
        message = f"BPM: {bpm}"
        client_socket.send(message.encode())

        # Receive response from the server
        response = client_socket.recv(1024)
        print('Server response:', response.decode())

        client_socket.close()
    except Exception as e:
        print('Failed to send data to server:', e)

async def main():
    while True:
        get_raw_values()
        process_values()

loop = asyncio.get_event_loop()
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occurred: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')

