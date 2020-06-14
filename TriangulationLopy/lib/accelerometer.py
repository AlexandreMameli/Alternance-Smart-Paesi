from   LIS2HH12 import LIS2HH12
from   machine  import Timer
import math

def acceleration(li = None, timeout = 0):
    if li == None:
        li = LIS2HH12()
    chrono     = Timer.Chrono()
    magnitudes = []
    average    = 0
    sum        = 0
    result     = 0
    if timeout <= 0:
        acceleration = li.acceleration()
        result       = math.sqrt(math.pow(acceleration[0], 2) +
                                 math.pow(acceleration[1], 2) +
                                 math.pow(acceleration[2], 2))
    else:
        chrono.start()
        while chrono.read() < timeout:
            acceleration = li.acceleration()
            magnitude    = math.sqrt(math.pow(acceleration[0], 2) +
                                     math.pow(acceleration[1], 2) +
                                     math.pow(acceleration[2], 2))
            magnitudes.append(magnitude)
        chrono.stop()
        for magnitude in magnitudes:
            sum += magnitude
        result = (sum / len(magnitudes))
    return result

def pitch(li = None):
    if li == None:
        li = LIS2HH12()
    return li.pitch()

def roll(li = None):
    if li == None:
        li = LIS2HH12()
    return li.roll()

def get_data(li = None, timeout = 0):
    if li == None:
        li = LIS2HH12()
    return (acceleration(li, timeout), pitch(li), roll(li))
