#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from machine import Pin, I2C
from lib.env import MPU925x, BME280, LTR390, TSL2591, SGP40
import VOC_Algorithm

class BME280Sensor: #Atmospheric Pressure/Temperature and humidity
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

class TSL2591Sensor: #LIGHT
    def __init__(self, i2c):
        self.sensor = TSL2591.TSL2591(i2c)
    
    def read_data(self):
        return {
            "lux": round(self.sensor.Lux(), 2)
        }

class LTR390Sensor: #UV
    def __init__(self, i2c):
        self.sensor = LTR390.LTR390(i2c)
    
    def read_data(self):
        return {
            "uvs": self.sensor.UVS()
        }

class SGP40Sensor: #Gas/O2 Concentration
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

class MPU925xSensor: #Gyroscope/Acceleration/Magnetometer
    def __init__(self, i2c):
        self.sensor = MPU925x.MPU925x(i2c)
    
    def read_data(self):
        icm = self.sensor.ReadAll()
        return {
            "acceleration": icm[:3],
            "gyroscope": icm[3:6],
            "magnetic": icm[6:9]
        }
