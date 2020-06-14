import ubinascii
from network import Bluetooth
from network import LoRa
import lora_connection
import functions
import socket
import time
import math
import csv
import pycom

lora = LoRa(mode = LoRa.LORA, tx_power = 14, sf = 9, coding_rate = LoRa.CODING_4_6)

sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
#sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
sock.setblocking(False)

datas = {}
while True:

    rc = sock.recv(64)
    if rc.decode().split(",")[0]=='tx 4-06':
        print(rc.decode().split(","))
        datas["id"] = rc.decode().split(",")[3]
        datas["lat"] = rc.decode().split(",")[1]
        datas["lon"] = rc.decode().split(",")[2]
        datas["rssi"] = lora.stats()[1]
        print(datas)
        csv.CSV.writeData2(data = datas)
        datas = {}
    #     message = b"GW 4-02, " + str(lora.stats()[1]).encode()
    #     print(message)
    #     sock.send(message)
    #     time.sleep(4)
    #     datas["GW1"] = lora.stats()[1]
    # if rc.decode().split(",")[0]=="GW 4-02" and "GW2" not in datas:
    #     datas["GW2"] = rc.decode().split(",")[1]
    # if rc.decode().split(",")[0]=="GW 4-10" and "GW3" not in datas:
    #     datas["GW3"] = rc.decode().split(",")[1]
    # print(datas)
    # if len(datas)==3:
    #     print(datas)
    #     csv.CSV.writeData2(data = datas)
    #     time.sleep(10)
    #     datas = {}
