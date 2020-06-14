from MPL3115A2 import MPL3115A2

ALTITUDE = const(0)
PRESSURE = const(1)

def altitude(mp = None):
    if  mp == None:
        mp = MPL3115A2(mode = ALTITUDE)
    return mp.altitude()

def pressure(mp = None):
    if  mp == None:
        mp = MPL3115A2(mode = PRESSURE)
    return mp.pressure()

def temperature(mp = None):
    if  mp == None:
        mp = MPL3115A2()
    return mp.temperature()

def get_data(mpa = None, mpp = None):
    if  mpa == None:
        mpa = MPL3115A2(mode = ALTITUDE)
    if  mpp == None:
        mpp = MPL3115A2(mode = PRESSURE)
    return (altitude(mpa), pressure(mpp), temperature(mpa))
