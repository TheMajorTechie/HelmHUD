#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import MPU925x #Gyroscope/Acceleration/Magnetometer
import BME280   #Atmospheric Pressure/Temperature and humidity
import LTR390   #UV
import TSL2591  #LIGHT
import SGP40
import VOC_Algorithm
import math
import machine

from machine import Pin, I2C
i2c = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26)) #I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

print("==================================================")
print("this is Environment Sensor test program...")
print("TSL2591 Light I2C address:0X29")
print("LTR390 UV I2C address:0X53")
print("SGP40 VOC I2C address:0X59")
print("MPU9250 9-DOF I2C address:0X68")
print("bme280 T&H I2C address:0X76")

devices = i2c.scan()
if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))
for device in devices:
    print("Hexa address: ",hex(device))



bme280 = BME280.BME280()
bme280.get_calib_param()
light = TSL2591.TSL2591()
sgp = SGP40.SGP40()
voc_sgp = VOC_Algorithm.VOC_Algorithm()
uv = LTR390.LTR390()
mpu = MPU925x.MPU925x()

try:
    while True:
#   time.sleep(1)
        bme = []
        bme = bme280.readData()
        pressure = round(bme[0], 2) 
        temp = round(bme[1], 2) 
        hum = round(bme[2], 2)
        
        lux = round(light.Lux(), 2)
        
        uvs = uv.UVS()
        
        gas = round(sgp.measureRaw(temp,hum), 2)
        voc = voc_sgp.VocAlgorithm_process(gas)
        icm = []
        icm = mpu.ReadAll()
        
        print("==================================================")
        print("pressure : %7.2f hPa" %pressure)
        print("temp : %-6.2f ℃" %temp)
        print("hum : %6.2f ％" %hum)
        print("lux : %d " %lux)
        print("uv : %d " %uvs)
        print("gas : %6.2f " %gas)
        print("VOC : %d " %voc)
        print("Acceleration: X = %d, Y = %d, Z = %d" %(icm[0],icm[1],icm[2]))
        print("Gyroscope:     X = %d , Y = %d , Z = %d" %(icm[3],icm[4],icm[5]))
        print("Magnetic:      X = %d , Y = %d , Z = %d" %(icm[6],icm[7],icm[8]))
        
except KeyboardInterrupt:
    exit()




