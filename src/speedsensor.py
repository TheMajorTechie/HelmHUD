#!/usr/bin/python
# -*- coding:utf-8 -*-
# This program uses the MPU9250 magnetometer on the Waveshare environment sensor to detect a magnet passing by.
# It then calculates the speed of the bike the magnet is on.

import time
import MPU925x  # Gyroscope/Acceleration/Magnetometer
import math

from machine import Pin, I2C

# Initialize I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

print("This is the Environment Sensor test program with speed calculation...")
print("MPU9250 9-DOF I2C address:0X68")

mpu = MPU925x.MPU925x()

icm = mpu.ReadAll()
x_new = icm[6]
z_new = icm[8]

#To have 4 or 8 cardinal directions on the compass
#1 = 4, 0 = 8
directions = True

# Constants
MAX_SPEED_MPH = 48.0  # Speed threshold for baseline reset
SPEED_CONVERSION_FACTOR = 5.17648788  # Pre-calculated factor based on circumference and conversion to mph
SLEEP_DURATION = 0.001  # Sleep duration in seconds (reduced for faster polling)

# Initialize variables
spike_threshold = 40000  # Adjust this value based on your setup
previous_time = None  # Initialize previous_time to None
magnet_detected = False  # State variable to track magnet detection

# Function to compute baseline manually
def compute_baseline(readings):
    print(compass(x_new, z_new))
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
        #elif x_value > 35000 and x_value <= 59000:
        #    direction = "North East"
        elif x_value > 500 and x_value <= 4000 and z_value > 2000 and z_value <= 6000:
            direction = "East"
        #elif x_value > 12500 and x_value <= 20000:
        #    direction = "South East"
        elif x_value > 11000 and x_value <= 14000 and z_value > 54000 and z_value <= 63000:
            direction = "South"
        #elif x_value > 6000 and x_value <= 10000:
        #    direction = "South West"
        elif x_value > 2000 and x_value <= 7000 and z_value > 48000 and z_value <= 54000:
            direction = "West"
        #elif x_value >= 0 and x_value <= 2000:
        #    direction = "North West"
        else:
            direction = "Unknown"
    else:
        if x_value > 58000 and x_value <= 63000 and z_value > 57000 and z_value <= 62000:
            direction = "North"
        elif x_value > 4000 and x_value <= 8000 and z_value > 1000 and z_value <= 10000:
            direction = "North East"
        elif x_value > 500 and x_value <= 4000 and z_value > 2000 and z_value <= 6000:
            direction = "East"
        elif x_value > 8000 and x_value <= 10999 and z_value > 57000 and z_value <= 62000:
            direction = "South East"
        elif x_value > 11000 and x_value <= 14000 and z_value > 59000 and z_value <= 63000:
            direction = "South"
        elif x_value > 6000 and x_value <= 10000 and z_value > 57000 and z_value <= 62000:
            direction = "South West"
        elif x_value > 2000 and x_value <= 7000 and z_value > 48000 and z_value <= 54000:
            direction = "West"
        elif x_value >= 7000 and x_value <= 14000 and z_value > 50000 and z_value <= 60000:
            direction = "North West"
        else:
            direction = "Unknown"
    return direction


# Collect baseline readings
print("Collecting baseline data...")
baseline = reset_baseline()

while True:
    icm = mpu.ReadAll()
    magnetic_field = icm[6:9]  # Extract magnetic field data

    # Compute the difference from baseline
    diff = [magnetic_field[i] - baseline[i] for i in range(3)]
    diff_magnitude = max(abs(diff[i]) for i in range(3))

    if not magnet_detected:
        # Check for spike indicating magnet is close
        if diff_magnitude > spike_threshold:
            current_time = time.ticks_us()
            if previous_time is not None:
                time_difference = time.ticks_diff(current_time, previous_time) / 1e6  # Convert microseconds to seconds

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
                        print(f"Speed: {speed_mph:.2f} mph")
                        previous_time = current_time
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
