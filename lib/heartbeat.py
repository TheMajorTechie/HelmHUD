import machine
import time
import bluetooth
from ble_advertising import advertising_payload
from MAX30102 import MAX30102

# Connect MAX30102 Heartrate sensor to SDA (Pin 4) and SCL (Pin 5)
SDA = 4
SCL = 5

# Define the UUIDs
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)

# Initialize I2C and MAX30102 sensor
i2c = machine.I2C(0, sda=machine.Pin(SDA), scl=machine.Pin(SCL))
sensor = MAX30102(i2c)

class BLESimplePeripheral:
    def __init__(self, ble, name="HelmHUD_HeartRate"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == bluetooth.IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == bluetooth.IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            self._advertise()
        elif event == bluetooth.IRQ_GATTS_WRITE:
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

def read_heart_rate():
    while True:
        red, ir = sensor.read_sequential()  # Read data from the sensor
        heart_rate = calculate_heart_rate(ir)  # Implement your own heart rate calculation logic
        if heart_rate:
            yield str(heart_rate)

def calculate_heart_rate(ir_values):
    # Implement a method to calculate heart rate from IR values
    # This is a placeholder function. You'll need to use an appropriate algorithm.
    return 75  # Placeholder value for heart rate

def main():
    ble = bluetooth.BLE()
    p = BLESimplePeripheral(ble)

    hr_gen = read_heart_rate()

    while True:
        if p.is_connected():
            try:
                heart_rate = next(hr_gen)
                print("Sending heart rate:", heart_rate)
                p.send(heart_rate)
            except StopIteration:
                break
        time.sleep(1)

if __name__ == "__main__":
    main()
