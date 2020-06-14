from SI7006A20 import SI7006A20

def temperature(si = None):
    if si == None:
        si = SI7006A20()
    return si.temperature()

def humidity(si = None):
    if si == None:
        si = SI7006A20()
    return si.humidity()

def dew_point(si = None):
    if si == None:
        si = SI7006A20()
    return si.dew_point()

def get_data(si = None):
    if si == None:
        si = SI7006A20()
    return (temperature(si), humidity(si), dew_point(si))
