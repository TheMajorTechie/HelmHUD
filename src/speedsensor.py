#!/usr/bin/python
# -*- coding:utf-8 -*-
#This program uses the MPU925 magnetometer on the waveshare environment sensor to detect a magnet passing by.
#It then calculates the speed of the bike the magnet is on.

#spike_threshold needs to be fiddled with to work nicely.

import time
import MPU925x  # Gyroscope/Acceleration/Magnetometer
import math

from machine import Pin, I2C

# Initialize I2C
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

print("This is the Environment Sensor test program with speed calculation...")
print("MPU9250 9-DOF I2C address:0X68")

mpu = MPU925x.MPU925x()

# Constants
#CIRCUMFERENCE_MILES = 0.0014379133  # Pre-calculated circumference of the wheel in miles
MAX_SPEED_MPH = 50.0  # Speed threshold for baseline reset
SPEED_CONVERSION_FACTOR = 5.17648788  # Pre-calculated factor based on circumference and conversion to mph
SLEEP_DURATION = 0.01  # Sleep duration in seconds

# Initialize variables
spike_threshold = 40000  # Adjusted threshold based on observations
previous_time = time.ticks_us()
ignore_counter = 0  # Counter to ignore the next few readings

# Function to compute baseline manually
def compute_baseline(readings):
    return [sum(axis) / len(axis) for axis in zip(*readings)]

# Function to reset the baseline
def reset_baseline():
    baseline_readings = []
    for _ in range(10):
        icm = mpu.ReadAll()
        baseline_readings.append(icm[6:9])
        #time.sleep(SLEEP_DURATION)  # Short delay between readings
    new_baseline = compute_baseline(baseline_readings)
    print("New baseline established:", new_baseline)
    return new_baseline

# Collect baseline readings
print("Collecting baseline data...")
baseline = reset_baseline()

while True:
    icm = mpu.ReadAll()
    magnetic_field = icm[6:9]  # Extract magnetic field data

    # If ignore_counter is active, skip this reading
    if ignore_counter > 0:
        ignore_counter -= 1
        continue

    # Check for spikes
    if any(abs(magnetic_field[i] - baseline[i]) > spike_threshold for i in range(3)):
        current_time = time.ticks_us()
        time_difference = time.ticks_diff(current_time, previous_time) / 1e6  # Convert microseconds to seconds
        time_difference += SLEEP_DURATION  # Add the sleep duration to the time difference
        
        # Ensure valid time difference for speed calculation
        if time_difference > 0:
            # Calculate speed in mph
            speed_mph = SPEED_CONVERSION_FACTOR / time_difference
            
            # Check if speed exceeds the threshold
            if speed_mph > MAX_SPEED_MPH:
                print(f"Speed exceeded {MAX_SPEED_MPH:.2f} mph. Resetting baseline.")
                baseline = reset_baseline()
            else:
                print(f"Rotation detected!")
                print(f"Speed: {speed_mph:.2f} mph")
            
            previous_time = current_time
            
            # Activate ignore_counter to skip the next 20 readings
            ignore_counter = 20

    time.sleep(SLEEP_DURATION)  # Adjusted sleep duration for consistency

