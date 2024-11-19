from machine import Pin, UART, Timer
import time

rxdata = ""
SENSOR_TYPE_GENARRAY_COMMANDS = ["type", "poll", "pressure", "temp", "hum", "lux", "uvs", "gas", "voc", "acc", "gyr", "mag", "hr"]

_SENSOR_TYPE_NONE = "0"		#default
_SENSOR_TYPE_GENARRAY = "1"
_SENSOR_TYPE_GPS = "2"

command_queue_index = 0
connected_sensor_type = "0"
current_command = "none"
ready_next_command = True

#poll the sensors present in the sensor companion pico
def poll_sensors(cb):
    global command_queue_index, current_command, connected_sensor_type, ready_next_command
    print("Polling sensors: Sensor type is ", connected_sensor_type)
    if connected_sensor_type is _SENSOR_TYPE_NONE:
        current_command = "type"
        uart.write(current_command)
        time.sleep_ms(100)
    elif connected_sensor_type is _SENSOR_TYPE_GENARRAY and ready_next_command:							#Generic sensor array code
        current_command = SENSOR_TYPE_GENARRAY_COMMANDS[command_queue_index]
        print("Command index: ", command_queue_index, "(", current_command, ")")
        if current_command == "poll":													#If we're polling, make sure we're not doing anything
            ready_next_command = False
        uart.write(current_command)
        command_queue_index += 1
        if command_queue_index > len(SENSOR_TYPE_GENARRAY_COMMANDS) - 1:				#Loop back to the beginning of the array
            #time.sleep_ms(10000)
            command_queue_index = 0
    #rx_data()

def clear_status_commands():
        global current_command#, ready_next_command
        current_command = "none"
    
def rx_data(cb):
    global rxdata, current_command, connected_sensor_type, ready_next_command
    if uart.any():
        rxdata = uart.read().decode()
        print(rxdata)
        if current_command == "type":
            connected_sensor_type = str(rxdata, 'utf8')
            clear_status_commands()
            print("Current type now set to: ", connected_sensor_type)        
        elif current_command == "temp":
            print("Temp: ", str(rxdata, 'utf8'), "℃")
            clear_status_commands()
        elif current_command == "pressure":
            print("Pressure: ", str(rxdata, 'utf8'))
            clear_status_commands()
        elif rxdata == "polling complete":
            ready_next_command = True
        else:
            print("Requested: ", current_command, ", Received: ", str(rxdata, 'utf8'))
            clear_status_commands()


#uart interrupts are not supported
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart.init(bits=8, parity=None, stop=2)

tim = Timer(period=500, mode=Timer.PERIODIC, callback=poll_sensors)
time.sleep_ms(100)
tim2 = Timer(period=500, mode=Timer.PERIODIC, callback=rx_data)




#while True:
#    if uart.any():
#        data = uart.read().decode()
#        print(data)
#        if data== '5':
#            print("received a 5. responding now")
#            uart.write("Sent a 5")