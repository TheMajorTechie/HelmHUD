#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from machine import Pin, I2C
from lib.env import BME280, TSL2591, LTR390, SGP40, MPU925x
import VOC_Algorithm

class TempSensor:  # Atmospheric Pressure/Temperature and humidity
    def __init__(self, i2c):
        self.sensor = BME280.BME280(i2c)
        self.sensor.get_calib_param()
    
    def read_data(self):
        bme = self.sensor.readData()
        return {
            "pressure": round(bme[0], 2),
            "temperature": round(bme[1], 2),
            "humidity": round(bme[2], 2)
        }

class LightSensor:  # LIGHT
    def __init__(self, i2c):
        print("Running")
        self.sensor = LightSensor(i2c)
        #self.sensor = LightSensor.TSL2591(i2c)
    
    def read_data(self):
        return {
            "lux": round(self.sensor.Lux(), 2)
        }

class UVSensor:  # UV
    def __init__(self, i2c):
        self.sensor = LTR390.LTR390(i2c)
    
    def read_data(self):
        return {
            "uvs": self.sensor.UVS()
        }

class GasSensor:  # Gas/O2 Concentration
    def __init__(self, i2c):
        self.sensor = SGP40.SGP40(i2c)
        self.voc_sgp = VOC_Algorithm.VOC_Algorithm()
    
    def read_data(self, temperature, humidity):
        gas = round(self.sensor.measureRaw(temperature, humidity), 2)
        voc = self.voc_sgp.VocAlgorithm_process(gas)
        return {
            "gas": gas,
            "voc": voc
        }

class Gyroscope:  # Gyroscope/Acceleration/Magnetometer
    def __init__(self, i2c):
        self.sensor = MPU925x.MPU925x(i2c)
    
    def read_data(self):
        icm = self.sensor.ReadAll()
        return {
            "acceleration": icm[:3],
            "gyroscope": icm[3:6],
            "magnetic": icm[6:9]
        }