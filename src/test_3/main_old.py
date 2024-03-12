# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-ssd1306-oled-micropython/

import machine
import utime
import ssd1306

#the LED is on the specialty 'LED' pin for the pico w
led = machine.Pin('LED', machine.Pin.OUT)

#You can choose any other combination of I2C pins
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4))


oled_width = 128
oled_height = 64
#oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=0x3c)
oled = ssd1306.SSD1306_I2C(128, 64, machine.I2C(0))

oled.text('Hello, World 1!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)

oled.show()

while True:
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(1)


print("finished printing")