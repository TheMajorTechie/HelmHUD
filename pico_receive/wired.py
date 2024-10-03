from lib.env import envsense_wrapper
from lib.max30102 import heartrate_wrapper
#import lib.ssd1306 as ssd1306
import machine

# i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
# oled_width = 128
# oled_height = 32
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)
# oled.text('HelmHUD', 0, 0)
# oled.text('Sensor', 0, 10)
# oled.text('Collator', 0, 20)
# oled.show()

i2c_central = machine.I2C(1, scl=machine.Pin(27), sda=machine.Pin(26))
envSensors = envsense_wrapper.EnvSenseWrapper(i2c_central)          #this is the central environmental sensor wrapper!
heartSensor = heartrate_wrapper.heartrate(i2c_central)                #this is the heartrate reader sensor!

packedArray = ""
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

heartSensor.get_readings()
heartrate = heartSensor.process_values()

sensorArray = [bme, lux, uvs, sgp, icm, heartrate]

packedArray = str(sensorArray)

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
print("Heart rate:  %d" %heartrate)

print("Main.py finished execution!")

print("Final array:")
print(packedArray)