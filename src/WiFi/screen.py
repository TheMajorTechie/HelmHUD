import machine
import time
import network
import socket
import lib.ssd1306 as ssd1306

# Set up I2C for OLED
i2c_display = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)

# Scan I2C bus to find the OLED's address
print("Scanning I2C bus...")
devices = i2c_display.scan()
if devices:
    print("I2C device addresses:", [hex(device) for device in devices])
    oled_addr = devices[0]  # Use the first found device
else:
    print("No I2C devices found")
    oled_addr = 0x3C  # Default address

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

def draw_symbol(oled, symbol):
    for y, row in enumerate(symbol):
        for x, pixel in enumerate(row):
            if ORIENTATION:
                oled.pixel(x + 123, y, pixel)  # Vertical Battery Position
            else:
                oled.pixel(x + 112, y, pixel)  # Horizontal Battery Position
    # Remove oled.show() to control updates from the main loop

def draw_text_rotated(oled, text, x, y):
    # Loop through each character in the text
    for i, char in enumerate(text):
        char_x = x + i * 8  # Calculate character's original x position
        char_y = y  # Original y position

        # Flip the coordinates for 180-degree rotation
        rotated_x = oled_width - char_x - 8
        rotated_y = oled_height - char_y - 8

        # Draw each character flipped by rendering it at the new rotated position
        oled.text(char, rotated_x, rotated_y)
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

print(AP_SSID)
print('Access Point Active')
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
latest_bpm = None
latest_speed = None
latest_direction = None 

# Main loop
while True:
    current_time = time.time()
    
    # Check if 2 hours have passed
    if current_time - start_time >= 2 * 3600:  # 2 hours in seconds
        battery_bars -= 1  # Decrease one bar
        if battery_bars < 0:
            battery_bars = 0
        start_time = current_time  # Reset the start time

    # Update the display
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

    # Display the latest BPM and Speed
    if latest_bpm is not None:
        oled.text(latest_bpm + ' bpm', 80, 25)
    else:
        oled.text('-- bpm', 80, 25)

    if latest_speed is not None:
        oled.text(latest_speed + ' mph', 0, 25)
    else:
        oled.text('-- mph', 0, 25)
        
    # Display Direction
    if latest_direction is not None:
        oled.text(latest_direction, 40, 0)
    else:
        oled.text('', 40, 0)

    oled.show()

    # Accept incoming connections
    try:
        print('Waiting for client connection...')
        client, addr = server.accept()
        print('Client connected from', addr)
        data = client.recv(1024)
        message = data.decode()
        print('Received:', message)

        # Process the message
        if message.startswith('BPM: '):
            latest_bpm = message[5:].strip()
        elif message.startswith('Speed: '):
            # Split the message to extract speed and direction
            lines = message.split('\n')
            speed_line = lines[0]
            direction_line = lines[1] if len(lines) > 1 else 'Direction: Unknown'

            latest_speed = speed_line[7:].strip()
            if direction_line.startswith('Direction:'):
                latest_direction = direction_line[10:].strip()
            else:
                latest_direction = 'Unknown'
        else:
            print('Unknown message format')
        
        # Send acknowledgment
        client.send('Acknowledged'.encode())
        client.close()
    except OSError as e:
        # Handle timeout exception
        pass
    except Exception as e:
        print('Server exception:', e)
        pass

