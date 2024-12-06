import machine
import time
import network
import socket
import lib.ssd1306 as ssd1306

# Set up I2C for OLED
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)

# Define constants and variables for your display
ORIENTATION = False
TRANSPARENT = False

# Initialize OLED based on the TRANSPARENT flag
if TRANSPARENT:
    oled_width = 128
    oled_height = 64  # Transparent OLED uses 128x64 resolution
    oled_addr = 0x3D  # I2C address for SSD1309 display
else:
    oled_width = 128
    oled_height = 32  # Old display uses 128x32 resolution
    oled_addr = 0x3C  # I2C address for SSD1306 display

# Initialize the OLED display with the selected address and dimensions
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_display, addr=oled_addr)

def flip_display(oled): # Needed for mounting physical display upside down.
    # Set display to normal orientation
    oled.write_cmd(0xA0)  # Segment remap normal
    oled.write_cmd(0xC0)  # COM scan direction normal

# Flip the display after initialization
flip_display(oled)

def draw_symbol(oled, symbol):
    for y, row in enumerate(symbol):
        for x, pixel in enumerate(row):
            if ORIENTATION:
                oled.pixel(x + 123, y, pixel)  # Vertical Battery Position
            else:
                oled.pixel(x + 112, y, pixel)  # Horizontal Battery Position
    # Remove oled.show() to control updates from the main loop

# Initialize with 3 battery bars
battery_bars = 3
start_time = time.time()

# Define battery symbols
HORIZ_FULL = [  # Horizontal Battery symbol with 3 bars
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

HORIZ_MED = [  # Horizontal Battery symbol with 2 bars
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

HORIZ_LOW = [  # Horizontal Battery symbol with 1 bar
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

HORIZ_EMPTY = [  # Horizontal Empty Battery Symbol
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

VERT_FULL = [  # Vertical Battery symbol with three bars
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]

VERT_MED = [  # Vertical Battery symbol with 2 bars
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]

VERT_LOW = [  # Vertical Battery symbol with 1 bar
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]

VERT_EMPTY = [  # Vertical Empty Battery symbol
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]

# --- Access Point Setup ---
# Define SSID for the AP
AP_SSID = 'PicoAP4'

# Initialize the Access Point interface
ap = network.WLAN(network.AP_IF)
ap.active(False)
ap.config(essid=AP_SSID, security=0)
ap.active(True)

# Wait for the AP interface to be active
while not ap.active():
    time.sleep(1)

print(AP_SSID + ' Active')
print('Network config:', ap.ifconfig())

# --- Server Setup ---
# Create a socket and bind to the AP's IP and a port
addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(5)
server.settimeout(0.5)  # Set a timeout for accept()

print('Server listening on', addr)

# Variables to store the latest data from clients
latest_bpm = 0
latest_speed = 0
latest_direction = 0
latest_temp = 0
latest_lat = 0
latest_long = 0

# Main loop
while True:
    current_time = time.time()
    
    # Check if 2 hours have passed
    if current_time - start_time >= 2 * 3600:  # 2 hours in seconds
        battery_bars -= 1  # Decrease one bar
        if battery_bars < 0:
            battery_bars = 0
        start_time = current_time  # Reset the start time

    # Update the Battery Icon
    oled.fill(0)  # Clear the display

    if ORIENTATION:
        if battery_bars == 3:
            draw_symbol(oled, VERT_FULL)
        elif battery_bars == 2:
            draw_symbol(oled, VERT_MED)
        elif battery_bars == 1:
            draw_symbol(oled, VERT_LOW)
        else:
            draw_symbol(oled, VERT_EMPTY)
    else:
        if battery_bars == 3:
            draw_symbol(oled, HORIZ_FULL)
        elif battery_bars == 2:
            draw_symbol(oled, HORIZ_MED)
        elif battery_bars == 1:
            draw_symbol(oled, HORIZ_LOW)
        else:
            draw_symbol(oled, HORIZ_EMPTY)

    # Update the other stats
    if latest_bpm: # Heartrate
        oled.text(latest_bpm + ' bpm', 80, oled_height-8)
    else:
        oled.text('-- bpm', 80, oled_height-8)

    if latest_speed: # Speed
        oled.text(latest_speed + ' mph', 0, oled_height-8)
    else:
        oled.text('-- mph', 0, oled_height-8)
        
    if latest_temp: # Temperature
        oled.text(latest_temp + 'F', 0, 0)
    else:
        oled.text('--', 0, 0)
        
    if latest_direction: # Direction
        oled.text(latest_direction, 61, 0)
    else:
        oled.text('--', 61, 0)
    
    if latest_lat: # GPS
        oled.text('Lat:' + latest_lat, 5, 12)
    else:
        oled.text('Lat: --', 5, 12)

    if latest_long:
        oled.text('Lon:' + latest_long, 5, 20)
    else:
        oled.text('Lon: --', 5, 20)

    oled.show()

    # Accept incoming connections
    try:
        #print('Waiting for client connection...')
        client, addr = server.accept()
        print('Client connected from', addr)
        data = client.recv(1024)
        message = data.decode()
        print('Received:', message)

        # Process the message
        if message.startswith('BPM: '):
            latest_bpm = message[5:].strip()
        elif message.startswith('Speed: '):
            # Split the message to extract speed, direction, and temp
            lines = message.split('\n')
            speed_line = lines[0]
            direction_line = ''
            temp_line = ''

            # Check for direction and temperature in the remaining lines
            for line in lines[1:]:
                if line.startswith('Direction:'):
                    direction_line = line
                elif line.startswith('Temp:'):
                    temp_line = line

            latest_speed = speed_line[7:].strip()

            if direction_line:
                latest_direction = direction_line[10:].strip()
            else: # Do nothing
                latest_direction = ''

            if temp_line:
                latest_temp = temp_line[6:].strip()
            #else: # Do nothing
            #    latest_temp = ''
        elif message.startswith('Temp: '):
            latest_temp = message[6:].strip()
            
        elif message.startswith('Lat: '):
            # Split GPS message
            lines = message.split('\n')
            lat_line = lines[0]
            long_line = ''
            
            for line in lines[1:]:
                if line.startswith('Lat:'):
                    lat_line = line
                elif line.startswith('Long:'):
                    long_line = line

            latest_lat = lat_line[5:].strip()

            if long_line:
                latest_long = long_line[6:].strip()
            else: # Do nothing
                latest_long = ''
        else:
            print('Unknown message format')

        # Send acknowledgment
        client.send('Acknowledged'.encode())
        client.close()
    except OSError as e:
        # Handle timeout exception
        pass
    except Exception as e: # Most likely need to restart everything
        print('Server exception:', e)
