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
    floats.append(data["temperature_b"])
    floats.append(data["pressure"])
    floats.append(data["altitude"])
    floats.append(data["temperature_t"])
    floats.append(data["humidity"])
    floats.append(data["dew_point"])
    floats.append(data["blue"])
    floats.append(data["red"])
    result += struct.pack(">12f", *floats)
    result += b'\r\n'
    return result
