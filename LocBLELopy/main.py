import ubinascii
from network import Bluetooth
from network import LoRa
import lora_connection
import functions
import socket

### BLE
bluetooth = Bluetooth()
### LoRa
lora = LoRa(mode = LoRa.LORAWAN)
lora.power_mode(LoRa.TX_ONLY)

lora_connection.loraConnection(lora)

srv = bluetooth.service(uuid=0xAAAA)
chr1 = srv.characteristic(uuid=0xBBBB, value=6)
bluetooth.set_advertisement(name="leLopy", manufacturer_data="lopy_v1")
bluetooth.advertise(True)
data = {}
data["nFinished"] = 0
data["lat"] = 0.0
data["lng"] = 0.0
data["date"] = 20200129
data["time"] = 100000
data["battery"] = 0
data["acceleration"] = 0
data["pitch"] = 0
data["roll"] = 0

# bluetooth.start_scan(60)
# while bluetooth.isscanning():
#     adv = bluetooth.get_adv()
#     if adv:
#         print(ubinascii.hexlify(bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)))

def conn_cb (bt_o):
    events = bt_o.events()   # this method returns the flags and clears the internal registry
    if events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

bluetooth.advertise(True)

sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
sock.setblocking(True)
temp = chr1.value()
print(temp)
request = None

while True:
    if temp != chr1.value():
        test = chr1.value().decode()
        print(test)
        loc = test.split(",")
        data["lat"] = float(loc[0])
        data["lng"] = float(loc[1])
        ### [5] Format the data and send it
        request = functions.formatRequest(data)
        try:
            sock.send(request)
        except:
            pass
    temp = chr1.value()
