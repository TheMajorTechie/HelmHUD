import machine
import bluetooth
import utime
import ssd1306
from ble_simple_peripheral import BLESimplePeripheral

#the LED is on the specialty 'LED' pin for the pico w
led = machine.Pin('LED', machine.Pin.OUT)
led_state = 0

adc = machine.ADC(4)

ble = bluetooth.BLE()

simplePeriph = BLESimplePeripheral(ble)

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, machine.I2C(0))	#default address 0x3c for ssd1306

oled.text('Hello, World 1!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)
screen1_row1 = 'row1'
screen1_row2 = 'row2'
screen1_row3 = 'row3'

oled.show()

led.value(0)

#A callback for the simple bluetooth peripheral that we call on receiving data
def on_SPCbRx(data):
    decoded_data = data.decode("utf-8")[:len(data)-2]
    print("Data received: ", data)
    global led_state
    if data == b'toggle\r\n':
        led.value(not led_state)
        led_state = 1 - led_state
    else:
        print("Non LED command. Printing to OLED and BT console.")
        #show_text(decoded_data, 0, 10)
        global screen1_row1
        screen1_row1 = decoded_data

#the weakness of this current method is that text gets overwritten when trying to
#display both temperature and BT data at once!
def show_text(text, position_x, position_y):
    oled.fill(0)
    for char in text:		# show text character by character for a neat effect
        utime.sleep(0.250)
        simplePeriph.send(str(char))
        oled.text(str(char), position_x, position_y)
        position_x += 8
        oled.show()
    simplePeriph.send('\r\n')
    
def scroll_screen_in_out(screen):
  for i in range (0, (oled_width+1)*2, 1):
    for line in screen:
      oled.text(line[2], -oled_width+i, line[1])
    oled.show()
    if i!= oled_width:
      oled.fill(0)
        
def refresh_temp_display(temp_c, temp_f):
    tempdisp = "Temps: {}C, {}F".format(temp_c,temp_f)
    #show_text(tempdisp, 0, 0)
    global screen1_row2
    screen1_row2 = tempdisp
    utime.sleep_ms(500)

screen1 = [[0, 0 , screen1_row1], [0, 10, screen1_row2], [0, 20, screen1_row3]]
scroll_screen_in_out(screen1)

while True:
    if simplePeriph.is_connected():
        simplePeriph.on_write(on_SPCbRx)
    ADC_v = adc.read_u16() * (3.3/65536)
    temp_c = 27 - (ADC_v - 0.706)/0.001721
    temp_f = 32 + (1.8*temp_c)
    refresh_temp_display(str(temp_c)[:4], str(temp_f)[:4])
    screen1 = [[0, 0 , screen1_row1], [0, 10, screen1_row2], [0, 20, screen1_row3]]
    scroll_screen_in_out(screen1)
    
        
        


