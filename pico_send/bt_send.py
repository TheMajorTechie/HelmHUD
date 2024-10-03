# Adapted from https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_uart_peripheral.py

import bluetooth
from lib.ble_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    #_FLAG_NOTIFY,
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    #_FLAG_WRITE,
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

# org.bluetooth.characteristic.gap.appearance.xml
#_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)


class BLEUART:        
    def __init__(self, ble, name="HH-uart", rxbuf=256):   #register BLE UART services
        #self._ble = ble
        #self._ble.active(True)
        #self._ble.irq(self._irq)
        #((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        #self._connections = set()
        #self._ble.config(mtu=256)							#increase the number of bytes that can be sent from the default of 20
        #self._write_callback = None
        #self._payload = advertising_payload(name=name, services=[_UART_UUID])
        #self._advertise()
        #self._rx_buffer = bytearray()
        #self._handler = None
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
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
        #elif event == _IRQ_GATTS_WRITE:
        #    conn_handle, value_handle = data
        #    value = self._ble.gatts_read(value_handle)
        #    if conn_handle in self._connections and value_handle == self._rx_handle:
        #        self._rx_buffer += self._ble.gatts_read(self._rx_handle)
        #        if self._handler:
        #            self._handler(value)
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)
        #elif event == _IRQ_GATTC_NOTIFY:
        #    conn_handle, value_handle, notify_data = data
        #    if conn_handle == self._conn_handle and value_handle == self._tx_handle:
        #        if self._notify_callback:
        #            self._notify_callback(notify_data)

    #def any(self):
    #    return len(self._rx_buffer)

    #def read(self, sz=None):
    #    if not sz:
    #        sz = len(self._rx_buffer)
    #    result = self._rx_buffer[0:sz]
    #    self._rx_buffer = self._rx_buffer[sz:]
    #    return result

    #def write(self, data):
    #    for conn_handle in self._connections:
    #        self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    #def close(self):
    #    for conn_handle in self._connections:
    #        self._ble.gap_disconnect(conn_handle)
    #    self._connections.clear()

    #def _advertise(self, interval_us=500000):
    #    self._ble.gap_advertise(interval_us, adv_data=self._payload)

    # Set handler for when data is received over the UART.
    #def on_notify(self, callback):
    #    self._notify_callback = callback
        
    #def on_write(self, callback):
    #    self._write_callback = callback
    
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

def demo():
    import time
    ble = bluetooth.BLE()
    uart = BLEUART(ble)
    #import wired
    #a dummy sensor data payload terminated with a newline
    sensorArray = [[813.79, 26.16, 23.84], 12.56, 0, [30779, 0], [-556, 144, -16168, 19, 70, 33, 9472, 36096, 56318], 0]
    packedArray = str(sensorArray)+"\n"

    def on_rx(v):
        print("RECEIVED DATA")
        #print("rx: ", uart.read().decode().strip())
        #print("RX", str(v, 'utf8'))
        print("RX", v)
        
    #uart.irq(handler=on_rx)
    #uart.on_notify(on_rx)
    uart.on_write(on_rx)

    #try:
    #    while True:
    #        uart.write(packedArray)
            #print("rx: ", uart.read().decode().strip())
            #uart.write(str(wired.bme))
    #except KeyboardInterrupt:
    #    pass

    while True:
        if uart.is_connected():
            # Short burst of queued notifications.
            #for _ in range(3):
            #    data = str(i) + "_"
            #    print("TX", data)
            #    uart.send(data)
            #    i += 1
            uart.send(packedArray)
        time.sleep_ms(100)

    #uart.close()


if __name__ == "__main__":
    demo()