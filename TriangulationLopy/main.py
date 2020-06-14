from network import Bluetooth
from network import LoRa
import lora_connection
import functions
import socket
import time

""" coeffs perte et rssi0 """
a = 50 #rssi0
n = 2.1 #coeff perte
""" """

""" locs gateways """
latgw1 = 9.0000
longw1 = 41.0000
latgw2 = 9.0000
longw2 = 41.0000
latgw3 = 9.0000
longw3 = 41.0000
""" """


### Bluetooth
bluetooth = Bluetooth()
srv = bluetooth.service(uuid=0xAAAA)
chr1 = srv.characteristic(uuid=0xBBBB, value=6)
bluetooth.set_advertisement(name="leLopy", manufacturer_data="lopy_v1")
bluetooth.advertise(True)

def conn_cb (bt_o):
    events = bt_o.events()   # this method returns the flags and clears the internal registry
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

bluetooth.advertise(True)

### LoRa
lora = LoRa(mode = LoRa.LORA, tx_power = 14, sf = 9, coding_rate = LoRa.CODING_4_6)
lora.power_mode(LoRa.TX_ONLY)
sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
sock.setblocking(False)
i = 0
test = chr1.value()
while True:
    if test != chr1.value():
        test = chr1.value()
        try:
            message = b'tx 4-06,' + test.decode() + ","+str(i)
            print(message)
            sock.send(message)
            i+=1
        except:
            pass
