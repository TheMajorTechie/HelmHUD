import machine
import bluetooth
import utime
import ssd1306
from ble_simple_peripheral import BLESimplePeripheral

#the LED is on the specialty 'LED' pin for the pico w
led = machine.Pin('LED', machine.Pin.OUT)
led_state = 0

ble = bluetooth.BLE()

simplePeriph = BLESimplePeripheral(ble)

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, machine.I2C(0))	#default address 0x3c for ssd1306

oled.text('Hello, World 1!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)

oled.show()

led.value(0)

#A callback for the simple bluetooth peripheral that we call on receiving data
def on_SPCbRx(data):
    print("Data received: ", data)
    global led_state
    if data == b'toggle\r\n':
        led.value(not led_state)
        led_state = 1 - led_state
    else:
        print("Non LED command. Printing to OLED and BT console.")
        oled.text(data, 0, 10)
        simplePeriph.send(data)
       

while True:
    if simplePeriph.is_connected():
        simplePeriph.on_write(on_SPCbRx)
        
        


