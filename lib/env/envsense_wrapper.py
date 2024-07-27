import MPU925x  #Gyroscope/Acceleration/Magnetometer
import BME280   #Atmospheric Pressure/Temperature and humidity
import LTR390   #UV
import TSL2591  #LIGHT
import SGP40
import VOC_Algorithm

class EnvSenseWrapper:
    def __init__(self, i2c):
        self.bme280 = BME280.BME280(i2c)        #atmospheric sensor
        self.bme280.get_calib_param()
        self.light = TSL2591.TSL2591(i2c)       #light sensor
        self.sgp = SGP40.SGP40(i2c)             #gas/O2
        self.voc_sgp = VOC_Algorithm.VOC_Algorithm()     #helper functions with sgp
        self.uv = LTR390.LTR390(i2c)            #UV
        self.mpu = MPU925x.MPU925x(i2c)         #9DOF physical measurement
    

    def read_out_bme(self):
        bme = []
        bme = self.bme280.readData()
        pressure = round(bme[0], 2)     #reads out values in hPa
        temp = round(bme[1], 2)         #reads out temps in degrees C
        hum = round(bme[2], 2)          #reads out as a humidity percentage

        return [pressure, temp, hum]    #easy to unpack array

    def read_out_light(self):
        lux = round(self.light.Lux(), 2)

        return lux

    def read_out_sgp(self):
        bme_readout = self.read_out_bme()
        gas = round(self.sgp.measureRaw(bme_readout[1],bme_readout[2]), 2)
        voc = self.voc_sgp.VocAlgorithm_process(gas)

        return [gas, voc]

    def read_out_uv(self):
        uvs = self.uv.UVS()

        return uvs

    def read_out_9dof(self):
        icm = []
        icm = self.mpu.ReadAll()

        #acceleration is the first 3 values in array (X, Y, Z)
        #gyroscope is the second set of 3
        #magnetic sensor is the final set of 3

        return icm