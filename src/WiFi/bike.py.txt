import time
import MPU925x  # Gyroscope/Acceleration/Magnetometer
from machine import Pin, I2C
import network  # Import network module for Wi-Fi
import socket   # Import socket module for networking
from lib.env import BME280

# --- Network Setup ---
# Define the SSID of the AP to connect to
AP_SSID = 'PicoAP4'

bme280 = BME280.BME280() #Atmospheric Pressure/Temperature and humidity
bme280.get_calib_param()

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

# Server IP is the IP address of the AP (usually 192.168.4.1)
SERVER_IP = '192.168.4.1'  # Replace with the actual IP if different
SERVER_PORT = 8080

# Initialize I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

print("This is the Environment Sensor test program with speed calculation...")
print("MPU9250 9-DOF I2C address:0X68")

mpu = MPU925x.MPU925x()

# Collect initial readings
icm = mpu.ReadAll()
x_new = icm[6]
z_new = icm[8]

# To have 4 or 8 cardinal directions on the compass
# True = 4 directions, False = 8 directions
directions = True

# Constants
MAX_SPEED_MPH = 48.0  # Speed threshold for baseline reset
SPEED_CONVERSION_FACTOR = 5.17648788  # Pre-calculated factor based on circumference and conversion to mph
SLEEP_DURATION = 0.001  # Sleep duration in seconds (reduced for faster polling)

# Initialize variables
spike_threshold = 10000  # Adjust this value based on your setup
previous_time = None  # Initialize previous_time to None
magnet_detected = False  # State variable to track magnet detection

def compute_temp():
    bme = []
    bme = bme280.readData()
    temp = round(bme[1], 2)
    temp = ((temp * 1.8) + 32)
    return temp

temp = compute_temp()

# Function to compute baseline manually
def compute_baseline(readings):
    return [sum(axis) / len(axis) for axis in zip(*readings)]

# Function to reset the baseline
def reset_baseline():
    baseline_readings = []
    for _ in range(10):
        icm = mpu.ReadAll()
        baseline_readings.append(icm[6:9])
        time.sleep(0.005)  # Short delay between readings
    new_baseline = compute_baseline(baseline_readings)
    print("New baseline established:", new_baseline)
    return new_baseline

def compass(x_value, z_value):
    if directions:
        if x_value > 58000 and x_value <= 63000 and z_value > 57000 and z_value <= 62000:
            direction = "North"
        elif x_value > 500 and x_value <= 4000 and z_value > 2000 and z_value <= 6000:
            direction = "East"
        elif x_value > 11000 and x_value <= 14000 and z_value > 54000 and z_value <= 63000:
            direction = "South"
        elif x_value > 2000 and x_value <= 7000 and z_value > 48000 and z_value <= 54000:
            direction = "West"
        else:
            direction = "Unknown"
    else:
        # Implement 8 directions if needed
        direction = "Unknown"
    return direction

# Collect baseline readings
print("Collecting baseline data...")
baseline = reset_baseline()

while True:
    icm = mpu.ReadAll()
    magnetic_field = icm[6:9]  # Extract magnetic field data

    x_new = magnetic_field[0]
    z_new = magnetic_field[2]

    # Compute the difference from baseline
    diff = [magnetic_field[i] - baseline[i] for i in range(3)]
    diff_magnitude = max(abs(diff[i]) for i in range(3))    

    if not magnet_detected:
        # Check for spike indicating magnet is close
        if diff_magnitude > spike_threshold:
            current_time = time.ticks_us()
            if previous_time is not None:
                time_difference = time.ticks_diff(current_time, previous_time) / 1e6  # Convert to seconds

                # Ensure valid time difference for speed calculation
                if time_difference > 0:
                    # Calculate speed in mph
                    speed_mph = round(SPEED_CONVERSION_FACTOR / time_difference)

                    # Check if speed exceeds the threshold
                    if speed_mph > MAX_SPEED_MPH:
                        print(f"Speed exceeded {MAX_SPEED_MPH:.0f} mph. Resetting baseline.")
                        baseline = reset_baseline()
                        previous_time = None  # Reset previous_time
                    else:
                        # Get the current direction
                        direction = compass(x_new, z_new)
                        print(f"Rotation detected!")
                        print(f"Speed: {speed_mph:.0f} mph, Direction: {direction}")
                        previous_time = current_time

                        # --- Send speed and direction data to server ---
                        try:
                            # Create a socket and connect to the server
                            client = socket.socket()
                            client.connect((SERVER_IP, SERVER_PORT))
                            
                            # Send speed and direction data to the server
                            message = f"Speed: {speed_mph:.0f}\nDirection: {direction}"
                            client.send(message.encode())

                            # Receive response from the server
                            response = client.recv(1024)
                            print('Server response:', response.decode())

                            client.close()
                        except Exception as e:
                            print('Failed to send data to server:', e)
                else:
                    # Invalid time difference
                    print("Invalid time difference detected.")
                    previous_time = current_time
            else:
                # First rotation detected
                print("First rotation detected, starting timer.")
                previous_time = current_time

            magnet_detected = True  # Set magnet_detected to True
    else:
        # Wait until magnetic field returns close to baseline
        if diff_magnitude < spike_threshold / 2:
            magnet_detected = False  # Reset magnet_detected

    time.sleep(SLEEP_DURATION)  # Short sleep to prevent high CPU usage
else:
    print(f"Access Point '{AP_SSID}' not found. Cannot proceed without network connection.")
