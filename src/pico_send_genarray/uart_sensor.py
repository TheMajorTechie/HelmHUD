from machine import Pin, UART
import time, random
import wired

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart.init(bits=8, parity=None, stop=2)

while True:
    if uart.any():
        rq = uart.read().decode()
        print(rq)
        if rq is "id":
            uart.write("HelmHUD Sensor Unit")
        elif rq is "type":
            uart.write("1")
            
        elif rq is "poll":
            uart.write("polling")
            wired.get_readouts()
            uart.write("polling complete")
            
        elif rq is "pressure":
            uart.write(str(wired.pressure))
            
        elif rq is "temp":
            uart.write(str(wired.temp))
            
        elif rq is "hum":
            uart.write(str(wired.hum))
            
        elif rq is "lux":
            uart.write(str(wired.lux))
            
        elif rq is "uvs":
            uart.write(str(wired.uvs))
            
        elif rq is "gas":
            uart.write(str(wired.gas))
            
        elif rq is "voc":
            uart.write(str(wired.voc))
            
        elif rq is "acc":
            uart.write("unimplemented")
        elif rq is "gyr":
            uart.write("unimplemented")
        elif rq is "mag":
            uart.write("unimplemented")
        elif rq is "hr":
            uart.write(str(wired.heartrate))
        elif rq is "heartbeat":
            uart.write("heartbeat acknowledged")
        else:
            print(rq)
            uart.write(str("Unexpected request: ", rq))
