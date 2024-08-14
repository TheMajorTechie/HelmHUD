from lib.env import envsense_wrapper
from lib.max30102 import heartrate_wrapper
#import lib.ssd1306 as ssd1306
import machine
import bluetooth
import random
import struct
import time
import machine
import ubinascii
from lib.ble_advertising import advertising_payload
from micropython import const

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

#Bluetooth stuff
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.general_activity_summary_data
_SENSE_CHAR = (
    bluetooth.UUID(0x2B3D),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,
)
_ENV_SENSE_SERVICE = (
    _ENV_SENSE_UUID,
    (_SENSE_CHAR,),
)

# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_SPORT_SENSE = const(5188)

#===============================================bluetooth class & helpers (based on picow_ble_temp_sensor from examples)
class BLESensors:
    def __init__(self, ble, name=""):
        self._sensor_readout = sensorsArray




        #self._sensor_temp = machine.ADC(4)
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        if len(name) == 0:
            name = 'Pico %s' % ubinascii.hexlify(self._ble.config('mac')[1],':').decode().upper()
        print('Sensor name %s' % name)
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID]
        )
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def update_values(self, notify=False, indicate=False):
        # Write the local value, ready for a central to read.
        #temp_deg_c = self._get_temp()
        #print("write temp %.2f degc" % temp_deg_c);
        sensorsArray = [bme, pressure, temp, hum, lux, uvs, sgp, gas, voc, icm, heartrate]

        self._ble.gatts_write(self._handle, struct.pack("<s", sensorsArray))
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    # Notify connected centrals.
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    # Indicate connected centrals.
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    # ref https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
    # def _get_temp(self):
    #     conversion_factor = 3.3 / (65535)
    #     reading = self._sensor_temp.read_u16() * conversion_factor
        
    #     # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    #     # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    #     return 27 - (reading - 0.706) / 0.001721

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

sensorsArray = [bme, pressure, temp, hum, lux, uvs, sgp, gas, voc, icm, heartrate]

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

ble = bluetooth.BLE()
BLESensor = BLESensors(ble)
counter = 0
while True:
    if counter % 10 == 0:
        BLESensor.update_values(notify=True, indicate=False)
    time.sleep_ms(1000)
    counter += 1