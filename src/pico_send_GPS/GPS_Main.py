import HelmHUD_GPS as GPS
import network
import socket
import time

#GPS setup
gps = GPS.HelmHUD_GPS()
gps.get_data()

# --- Network Setup ---
# Define the SSID of the AP to connect to
AP_SSID = 'PicoAP4'

# Initialize the Station interface
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Scan for available networks
picoFound = False
while not picoFound:
    networks = sta.scan()
    print('Available networks:')
    for net in networks:
        ssid = net[0].decode()
        print(ssid)

    # Check if 'PicoAP4' is in the list
    if AP_SSID not in [net[0].decode() for net in networks]:
        print(f"Access Point '{AP_SSID}' not found. Check if the AP is active and nearby.")
    else:
        print(f"Access Point '{AP_SSID}' found. Attempting to connect...")
        sta.connect(AP_SSID)
        picoFound = True
        # Wait for connection
        while not sta.isconnected():
            print('Connecting to network...')
            time.sleep(1)
    time.sleep(5)

print('Station Connected')
print('Network config:', sta.ifconfig())

# Server IP is the IP address of the AP (usually 192.168.4.1)
SERVER_IP = '192.168.4.1'  # Replace with the actual IP if different
SERVER_PORT = 8080

#will convert the GPS' 2 string array into a single string
def gps_data_single_string():
    return gps.data[0] + gps.data[1]

while True:
    gps.get_data()
    print("Attempting to send data:",gps_data_single_string())
    try: #send to server
        client = socket.socket()
        client.connect((SERVER_IP, SERVER_PORT))
        
        message = "Lat: "+gps.data[0]+"\nLong: "+gps.data[1]
        print("Message:",message)
        client.send(message.encode())
        
        response = client.recv(1024)
        print("Server response: ", response.decode())
        
        client.close()
    except Exception as e:
        print("Failed to send data to server:",e)
    
    time.sleep(5) #5 seconds for gps refresh