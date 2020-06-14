from   L76GNSS    import L76GNSS
import conf
import pycom

def wait_satellites(l76 = None):
    """Wait for satellites to be in view"""
    if l76 == None:
        l76 = L76GNSS(timeout = conf.GPS_TIMEOUT)
    while l76.check_satellites() == '00':
        pass

def set_GPS_timeout(l76 = None):
    """Set the GPS timeout according to the number of satellites in view"""
    if l76 == None:
        l76 = L76GNSS(timeout = conf.GPS_TIMEOUT)
    if l76.check_satellites() < '04' and pycom.nvs_get('gpscount') < 2:
        pycom.nvs_set('gpscount', pycom.nvs_get('gpscount') + 1)
        conf.DEEP_SLEEP_PERIOD = 150 # 2 minutes 30s
    elif l76.check_satellites() < '04':
        pycom.nvs_set('gpscount', 0)
        conf.DEEP_SLEEP_PERIOD = 900 # 15 minutes
    else:
        #latlng  = l76.coordinates(1)
        """
        if latlng[0] == None or latlng[1] == None:
            conf.GPS_TIMEOUT = 300
            conf.DEEP_SLEEP_PERIOD = 60 # 1 minute
            return True
        else:
            conf.DEEP_SLEEP_PERIOD = 300 # 15 minutes
            return True
        """
        return True
    return False

def coordinates(l76 = None):
    """Get latitude and longitude from GPS"""
    if l76 == None:
        l76 = L76GNSS(timeout = conf.GPS_TIMEOUT)
    try:
        latlng  =l76.coordinates()
        time    = int(latlng[2][6:])
        date    = int("20" + latlng[2][4:6] + latlng[2][2:4] + latlng[2][:2])
        return (latlng[0], latlng[1], date, time)
    except:
        return (None, None, None, None)

def getTime(l76 = None):
    if l76 == None:
        l76 = L76GNSS(timeout = conf.GPS_TIMEOUT)
    return l76.getTime()
