
import binascii
import struct

################################################################################
###
### FUNCTIONS
###

def threading(func, arg, data, key, lock):
    if type(arg) is list or type(arg) is tuple:
        result = func(*arg)
    else:
        result = func(arg)
    with lock:
        for i in range(len(key)):
            data[key[i]] = result[i]
        data["nFinished"] += 1

def formatRequest(data):
    """Transform values to bytes to be send by the device."""
    floats      = []
    datetime    = []
    gps         = []
    result      = b''
    floats.append(data["battery"])
    floats.append(data["acceleration"])
    floats.append(data["pitch"])
    floats.append(data["roll"])
    result += struct.pack(">4f", *floats)
    if data["date"] is not None:
        datetime.append(data["date"])
        datetime.append(data["time"])
        result += struct.pack(">2i", *datetime)
    if data["lat"] is not None:
        gps.append(data["lat"])
        gps.append(data["lng"])
        result += struct.pack(">2f", *gps)
    result += b'\r\n'
    return result
