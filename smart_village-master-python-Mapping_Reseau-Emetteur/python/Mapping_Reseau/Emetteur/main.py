from   pysense     import Pysense
from   network     import LoRa
from   LTR329ALS01 import LTR329ALS01
import accelerometer
import thermometer
import barometer
import lora_connection
import functions
import _thread
import machine
import socket
import csv
import time

################################################################################
###
### VARIABLES
###

### Threads
lock = _thread.allocate_lock()

### Data
request           = None
data              = dict()
data["nFinished"] = 0
try:
    count = pycom.nvs_get('count')
except:
    count = 0

### LoRa
lora = LoRa(mode = LoRa.LORA, tx_power = 14, sf = 9, coding_rate = LoRa.CODING_4_6)
lora.power_mode(LoRa.TX_ONLY)

### Pysense
py = Pysense()
lt = LTR329ALS01()
################################################################################
###
### MAIN PROGRAM
###

### [0] Initialize threads
params = []
#params.append((lora_connection.loraConnection, lora, data, [], lock))
#params.append((accelerometer.get_data, (None, 2), data,
#               ("acceleration", "pitch", "roll"), lock))
params.append((thermometer.get_data, None, data,
               ("temperature_t", "humidity", "dew_point"), lock))
params.append((barometer.get_data, None, data,
               ("altitude", "temperature_b", "pressure"), lock))
#params.append((lt.light, None, data, ("blue", "red"), lock))
### [1] Execute threads

while True:
    for param in params:
        _thread.start_new_thread(functions.threading, param)

    data["battery"] = py.read_battery_voltage()

    ### [2] Initialize socket
    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    #sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    sock.setblocking(False)

    ### [3] Wait for threads to finish
    while data["nFinished"] < len(params):
        pass

    ### [4] Format the data and send it
    #request = functions.formatRequest(data)
    for i in range(100):
        sock.send('012345678')
        time.sleep_ms(200)

    ### [5] Check for received data
    #lora_connection.receivedData(sock, pycom)

    ### [6] Save network data in the NVRAM
    lora.nvram_save()

    csv.CSV.writeData2(conf.MOUNT, str(count) + ".txt", None, [data['battery'],
            data['temperature_b'], data["pressure"], data["altitude"],
            data["temperature_t"], data["humidity"], data["dew_point"]])

    pycom.nvs_set('count', count + 1)

    pycom.rgbled(0x0000FF)
    time.sleep_ms(60000)
