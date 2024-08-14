# from lib.env import envsense_wrapper      #something's up with envsense and the ssd1306 display will not work if envsense_wrapper is even imported.
from lib.max30102 import heartrate_wrapper
import lib.ssd1306 as ssd1306
import machine

i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display)
oled.text('HelmHUD', 0, 0)
oled.text('Sensor', 0, 10)
oled.text('Collator', 0, 20)
oled.show()