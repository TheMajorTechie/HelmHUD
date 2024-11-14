# Adapted from https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_uart_peripheral.py

import bluetooth
from lib.ble_advertising import advertising_payload
import HelmHUD_GPS
from micropython import const
import _thread

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

class BLEUART:        
    def __init__(self, ble, name="HH-uart", rxbuf=256):   #register BLE UART services
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._rx_buffer = bytearray()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def irq(self, handler):
        self._handler = handler

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle in self._connections:
                self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)
    
    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)
        
    def is_connected(self):
        return len(self._connections) > 0
    
    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def on_write(self, callback):
        self._write_callback = callback

def hhuart_sender():
    import time
    ble = bluetooth.BLE()
    uart = BLEUART(ble)

    def on_rx(v):
        global time_since_command
        time_since_command = 0
        print("RECEIVED DATA")
        print("RX", v)
        rq = v.decode('UTF-8')
        if wired.sensor_polling is False:
            if rq is "id":
                uart.send("HelmHUD Sensor Unit")
                
            elif rq is "type":
                uart.send("2")	#GPS type
                
            elif rq is "GPS_r0":
                uart.send(str(HelmHUD_GPS.data[0]))
                
            elif rq is "GPS_r1":
                uart.send(str(HelmHUD_GPS.data[1]))
                
            else:
                print(rq)
                uart.send(str("Unexpected request: ", rq))
        else:
            print("Attempted to get sensor data during polling")
            uart.send("still_polling")
        
    uart.on_write(on_rx)
        

    while True:  
        wired.get_readouts()
        time.sleep_ms(10000)

if __name__ == "__main__":
    try:
        hhuart_sender()
    except KeyboardInterrupt:
        machine.reset()
    