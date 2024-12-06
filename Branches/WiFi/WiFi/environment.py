import time
import MPU925x  # Gyroscope/Acceleration/Magnetometer
from machine import Pin, I2C
import network  # Import network module for Wi-Fi
import socket   # Import socket module for networking
from lib.env import BME280

# --- Network Setup ---
# Define the SSID and password of the AP to connect to
AP_SSID = 'PicoAP4'

# Initialize the BME280 sensor
bme280 = BME280.BME280()  # Atmospheric Pressure/Temperature and humidity
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

    # To have 4 or 8 cardinal directions on the compass
    # True = 4 directions, False = 8 directions
    use_four_directions = True

    # Constants
    MAX_SPEED_MPH = 48.0  # Speed threshold for baseline reset
    SPEED_CONVERSION_FACTOR = 5.17648788  # Pre-calculated factor based on circumference and conversion to mph
    SLEEP_DURATION = 0.001  # Sleep duration in seconds (reduced for faster polling)

    # Initialize variables
    spike_threshold = 10000  # Adjust this value based on your setup
    previous_time = None  # Initialize previous_time to None
    magnet_detected = False  # State variable to track magnet detection
    current_direction = "Unknown"  # Initialize current_direction

    # Flag to ensure temperature is sent only once
    temp_sent = False

    def compute_temp():
        bme = bme280.readData()
        temp_c = bme[1]
        temp_f = (temp_c * 1.8) + 32
        temp_f = round(temp_f)
        return temp_f

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

        # Compute the current direction based on the last reading
        x_value = baseline_readings[-1][0]
        z_value = baseline_readings[-1][2]
        global current_direction
        current_direction = compass(x_value, z_value)
        print("Direction:", current_direction)
        return new_baseline

    def is_in_range(value, lower, upper):
        max_value = 65535
        if lower <= upper:
            return lower <= value <= upper
        else:
            # Handle wrap-around
            return value >= lower or value <= upper

    def compass(x_value, z_value):
        delta = 6000  # Adjust the range as needed
        max_value = 65535

        # Directions with new calibration values
        directions = {
            "North": {"x": 58000, "z": 58500},
            "East":  {"x": 2500,  "z": 65000},
            "South": {"x": 11500, "z": 58000},
            "West":  {"x": 65000, "z": 47000}
        }

        for direction, center in directions.items():
            x_center = center["x"]
            z_center = center["z"]

            # Calculate lower and upper bounds with wrap-around
            x_lower = (x_center - delta) % (max_value + 1)
            x_upper = (x_center + delta) % (max_value + 1)
            z_lower = (z_center - delta) % (max_value + 1)
            z_upper = (z_center + delta) % (max_value + 1)

            if is_in_range(x_value, x_lower, x_upper) and is_in_range(z_value, z_lower, z_upper):
                return direction

        return "Unknown"

    # Collect baseline readings
    print("Collecting baseline data...")
    baseline = reset_baseline()

    while True:
        # Send temperature once upon boot
        if not temp_sent:
            try:
                temp = compute_temp()
                message = f"Temp: {temp:.0f}"
                # Create a socket and connect to the server
                client = socket.socket()
                client.connect((SERVER_IP, SERVER_PORT))
                client.send(message.encode())
                # Receive response from the server
                response = client.recv(1024)
                print('Server response:', response.decode())
                client.close()
                temp_sent = True  # Set flag to True after sending temperature
                print(f"Temperature {temp}°F sent to server.")
            except Exception as e:
                print('Failed to send temperature to server:', e)

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
                        speed_mph = SPEED_CONVERSION_FACTOR / time_difference

                        # Check if speed exceeds the threshold
                        if speed_mph > MAX_SPEED_MPH:
                            print(f"Speed exceeded {MAX_SPEED_MPH:.2f} mph. Resetting baseline.")
                            baseline = reset_baseline()
                            previous_time = None  # Reset previous_time
                        else:
                            print(f"Rotation detected!")
                            print(f"Speed: {speed_mph:.2f} mph, Direction: {current_direction}")
                            previous_time = current_time

                            # --- Send speed and direction data to server ---
                            try:
                                # Create a socket and connect to the server
                                client = socket.socket()
                                client.connect((SERVER_IP, SERVER_PORT))

                                # Send speed and direction data to the server
                                message = f"Speed: {speed_mph:.2f}\nDirection: {current_direction}"
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


