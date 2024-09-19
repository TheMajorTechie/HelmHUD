import time
from machine import Pin

LED = machine.Pin("LED", Pin.OUT)
button = machine.Pin(15, Pin.IN, Pin.PULL_DOWN)

buttonPresses = 0 #Count of times the button has been pressed
lastPress = 0 #Last time we pressed the button

#Gets called every time the button is pressed.
def buttonPressed(pin):
    global buttonPresses, lastPress
    countTime = time.ticks_ms()
    if (countTime - lastPress) > 200: 
        buttonPresses += 1
        lastPress = countTime

button.irq(trigger=machine.Pin.IRQ_FALLING, handler = buttonPressed)

lastPress = 0
while True:
    if buttonPresses != lastPress:
        LED.toggle()
        lastPress = buttonPresses
