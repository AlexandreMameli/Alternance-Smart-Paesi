from   machine import Timer
from   csv     import CSV
import time
import gc
import binascii
import ure

import conf

class L76GNSS:
    """
        This class alows the usage of the L76GNSS component.
    """
    GPS_I2CADDR = const(0x10)

    def __init__(self, pytrack=None, sda='P22', scl='P21', timeout=None):
        if pytrack is not None:
            self.i2c = pytrack.i2c
        else:
            from machine import I2C
            self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl))
        self.chrono         = Timer.Chrono()
        self.timeout        = timeout
        self.timeout_status = True
        self.reg            = bytearray(1)
        self.i2c.writeto(GPS_I2CADDR, self.reg)

    def _read(self):
        """Read GPS data."""
        self.reg = self.i2c.readfrom(GPS_I2CADDR, 32)
        return self.reg

    def _getFrame(self, nmea):
        """Return the first nmea frame cointained in a string and the rest of the string."""
        if nmea != b"":
            m = ure.search('\$.*\*', nmea)
            if m != None:
                return (m.group(0).split(','), nmea[len(m.group(0)) + 4:])
        return (None, nmea)

    def _convert_coords(self, gngll_s):
        """Convert coordinates into a readable format."""
        try:
            lat_d = (float(gngll_s[1]) // 100) + ((float(gngll_s[1]) % 100) / 60)
            lon_d = (float(gngll_s[3]) // 100) + ((float(gngll_s[3]) % 100) / 60)
            if gngll_s[2] == 'S':
                lat_d *= -1
            if gngll_s[4] == 'W':
                lon_d *= -1
            return (lat_d, lon_d)
        except:
            return None

    def coordinates(self, t_listen = 10):
        """
            Return the current coordinates, date and timeself.

            Search for RMC, GLL and GSA messages. RMC gives time and date, GLL
            gives position and GSA gives the PDOP. Stop listening if no GLL
            message have been recieved in ``t_listen`` seconds.
        """

        nmea        = b""
        stop        = Timer.Chrono()
        counter     = Timer.Chrono()
        lat         = lng = pdop = 0
        latitudes   = []
        longitudes  = []
        pdops       = []
        gsa         = False
        rmc         = False
        datetime    = ''
        stop.start()
        # Start listening
        while stop.read() < self.timeout:
            # Get the next message to process
            nmea += self._read().lstrip(b'\n\n').rstrip(b'\n\n')
            frame, nmea = self._getFrame(nmea)
            #self.writeNMEA("sd", "nmea.txt", None, frame)
            # Process the message according to its type
            if frame != None:
                if frame[0].find("GLL") != -1:
                    stop.stop()
                    counter.start()
                # Check date and time
                elif not rmc and frame[0].find('RMC') != -1 and len(frame) > 9:
                    datetime = frame[9] + str(frame[1].split('.')[0])
                    rmc      = True
                # Analyse GSA and GLL messages
                if counter.read() < t_listen:
                    # Store PDOP
                    if gsa and frame[0].find('GSA') != -1 and len(frame) > 15:
                        if frame[15] != "":
                            pdops.append(frame[15])
                        else:
                            pdops.append("1000")
                        gsa = False
                    #Store coordinates
                    elif frame[0].find('GLL') != -1:
                        coord = self._convert_coords(frame)
                        if coord != None:
                            latitudes.append(coord[0])
                            longitudes.append(coord[1])
                            gsa = True
                # Mean and return coordinates values
                else:
                    lat = lng = pdop = 0
                    for i in range(len(pdops)):
                        coeff   = pow(1 / float(pdops[i]), 2)
                        lat     += coeff * latitudes[i]
                        lng     += coeff * longitudes[i]
                        pdop    += coeff
                    if pdop != 0:
                        return (lat/pdop, lng/pdop, datetime)
                    else:
                        break
                # Force garbage collection to avoid memory overload
                gc.collect()
        return (None, None, datetime)

    def check_satellites(self):
        """Return the number of satellites in view."""
        nmea    = b''
        stop    = Timer.Chrono()
        nb_sat  = '00'
        stop.start()
        # Start listening
        while stop.read() < self.timeout:
            # Get the next message to process
            nmea  += self._read().lstrip(b'\n\n').rstrip(b'\n\n')
            frame, nmea = self._getFrame(nmea)
            #self.writeNMEA("sd", "nmea.txt", None, frame)
            # Force garbage collection to avoid memory overload
            gc.collect()
            # Analyse GSV message
            if frame != None and frame[0].find('GSV') != -1 and len(frame) > 3:
                # Store the number of satellites in view
                nb_sat = frame[3]
                # Stop the process if more than 3 satellites are in view
                if frame[3] > '03':
                    break
        return nb_sat

    def getTime(self):
        """Return the GPS date and time."""
        nmea    = b''
        stop    = Timer.Chrono()
        date_time  = None
        stop.start()
        # Start listening
        while stop.read() < self.timeout:
            # Get the next message to process
            nmea  += self._read().lstrip(b'\n\n').rstrip(b'\n\n')
            frame, nmea = self._getFrame(nmea)
            #self.writeNMEA("sd", "nmea.txt", None, frame)
            # Force garbage collection to avoid memory overload
            gc.collect()
            # Analyse GSV message
            if frame != None and frame[0].find('RMC') != -1 and len(frame) > 9:
                datetime = frame[9] + str(frame[1].split('.')[0])
                break
        return datetime

    def writeNMEA(self, mount, file, head, data):
        """Write NMEA message in a file."""
        if CSV.mount(mount):
            if head != None and not file in os.listdir("/" + mount):
                CSV.write(head, mount, file)
            if isinstance(data, list):
                CSV.write(data, mount, file, mode = "a")
            elif isinstance(data, dict):
                CSV.writeFromDictionnary(data)
