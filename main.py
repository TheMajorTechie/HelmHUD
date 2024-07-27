from lib.env import envsense_wrapper
import machine

i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))

envSensors = envsense_wrapper.EnvSenseWrapper(i2c_central)          #this is the central environmental sensor wrapper!

#===============================================getting sensor readouts

bme = envSensors.read_out_bme()
pressure = round(bme[0], 2) 
temp = round(bme[1], 2) 
hum = round(bme[2], 2)

lux = round(envSensors.read_out_light(), 2)

uvs = envSensors.read_out_uv()

sgp = envSensors.read_out_sgp()
gas = sgp[0]
voc = sgp[1]
icm = envSensors.read_out_9dof()

#=============================================printing sensor readouts

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

print("Main.py finished execution!")